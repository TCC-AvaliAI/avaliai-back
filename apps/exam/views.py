from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Exam, ExamStatus
from .serializers import ExamSerializer, ExamListSerializer, ExamStatisticsSerializer, UpdateExamQRCodeSerializer
from apps.question.serializers import QuestionSerializer
from avaliai.ai_prompt import AIPrompt
import requests
from .services.exam_statistics import ExamStatisticsService
from .services.exam_html import ExamHTMLService
import pdfkit
from django.http import HttpResponse
from pdfkit.configuration import Configuration
from .services.exam_by_ai import ExamService
from avaliai.services.search_rapid_fuzz import SearchFuzzService
from uuid import UUID


class ExamListAndCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all exams",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Filter exams by title",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        query_serializer=ExamListSerializer,
        responses={
            200: ExamSerializer(many=True),
            400: "Bad Request - UUID inválido"
        }
    )
    def get(self, request):
        user = request.user
        serializer = ExamSerializer(data=request.GET)
        exams = Exam.objects.filter(user=user).select_related("user").order_by('-created_at')
        search = request.query_params.get('search', None)
        if search:
            exams = SearchFuzzService.fuzzy_filter(exams, search)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        paginated_exams = paginator.paginate_queryset(exams, request)
        serializer = ExamSerializer(paginated_exams, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new exam",
        request_body=ExamSerializer,
        responses={201: ExamSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ExamSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExamDetailUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve an exam by ID",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: ExamSerializer, 404: "Not Found"}
    )
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update an exam by ID",
        request_body=ExamSerializer,
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: ExamSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        serializer = ExamSerializer(exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an exam by ID",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        exam.delete()
        return Response({"message": "Exam deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class ExamQuestions(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all questions of an exam",
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        questions = exam.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Add a question to an exam",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question_id': openapi.Schema(type=openapi.TYPE_STRING, description="ID of the question")
            },
            required=['question_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "Question added to exam", 400: "Bad Request"}
    )
    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        question_id = request.data.get('question_id')
        if not question_id:
            return Response({"error": "question_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            question_uuid = UUID(question_id)
            if question_uuid in exam.questions.values_list('id', flat=True):
                return Response({"error": "Question already exists in exam"}, status=status.HTTP_400_BAD_REQUEST)
            exam.questions.add(question_id)
            return Response({"message": "Question added to exam"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)
        
class DetachQuestion(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Detach a question from an exam",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'question_id', openapi.IN_PATH, description="ID of the question", type=openapi.TYPE_STRING
            )
        ],
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, exam_id, question_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        try:
            question_uuid = UUID(question_id)
            if question_uuid not in exam.questions.values_list('id', flat=True):
                return Response({"error": "Question not found in exam"}, status=status.HTTP_404_NOT_FOUND)
            exam.questions.remove(question_uuid)
            return Response({"message": "Question detached from exam"}, status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)

class CreateExamByAI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new exam and generate questions using AI",
        request_body=ExamSerializer,
        responses={201: ExamSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ExamSerializer(data=request.data, context={'request': request})
        user = self.request.user
        if serializer.is_valid():
            data = serializer.validated_data
            prompt = AIPrompt(
                type=data.get('title', 'prova'),
                description=data.get('description', ''),
                discipline=data.get('discipline').name,
                theme=data.get('theme', ''),
                difficulty=data.get('difficulty', 'MEDIUM')
            ).ai_prompt
            try:
                return ExamService.create_exam_by_ai(serializer, prompt, user, data)
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExamDetails(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve exam statistics",
        responses={200: ExamStatisticsSerializer}
    )
    def get(self, request):
        user = request.user
        stats = ExamStatisticsService.get_exam_statistics(user)
        serializer = ExamStatisticsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateExamQRCode(APIView):
    @swagger_auto_schema(
        operation_description="Update exam QR code",
        request_body=UpdateExamQRCodeSerializer,
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: UpdateExamQRCodeSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        if(exam.qr_code != None):
            return Response({"error": "The qr code has already been generated"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('qr_code'):
            return Response({"error": "qr_code is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateExamQRCodeSerializer(exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExamPDFFile(APIView):
    @swagger_auto_schema(
        operation_description="Generate a PDF file of the exam",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "PDF file"}
    )
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)  
        if(exam.qr_code == None):
            return Response({"error": "The qr code has not been generated yet"}, status=status.HTTP_400_BAD_REQUEST)
        html_content = ExamHTMLService.generate_html_exam(exam)
        config = Configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdf = pdfkit.from_string(html_content, False, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{exam.title}.pdf"'
        return response
    


class MarkExamAsApplied(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mark an exam as applied",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "Exam marked as applied", 404: "Not Found"}
    )
    def patch(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        if(exam.status == ExamStatus.APPLIED):
            return Response({"message": "Exam already marked as applied"}, status=status.HTTP_400_BAD_REQUEST)
        exam.status = ExamStatus.APPLIED
        exam.save()
        return Response({"message": "Exam marked as applied"}, status=status.HTTP_200_OK)


class MarkExamAsArchived(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mark an exam as archived",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "Exam marked as archived", 404: "Not Found"}
    )
    def patch(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        if(exam.status == ExamStatus.ARCHIVED):
            return Response({"message": "Exam already marked as archived"}, status=status.HTTP_400_BAD_REQUEST)
        exam.status = ExamStatus.ARCHIVED
        exam.save()
        return Response({"message": "Exam marked as archived"}, status=status.HTTP_200_OK)
    
class MarkExamAsCanceled(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mark an exam as canceled",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
        responses={200: "Exam marked as canceled", 404: "Not Found"}
    )
    def patch(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        if(exam.status == ExamStatus.CANCELLED):
            return Response({"message": "Exam already marked as canceled"}, status=status.HTTP_400_BAD_REQUEST)
        exam.status = ExamStatus.CANCELLED
        exam.save()
        return Response({"message": "Exam marked as canceled"}, status=status.HTTP_200_OK)