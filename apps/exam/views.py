from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Exam
from .serializers import ExamSerializer
from apps.question.serializers import QuestionSerializer

class ExamListAndCreate(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all exams",
        responses={200: ExamSerializer(many=True)}
    )
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new exam",
        request_body=ExamSerializer,
        responses={201: ExamSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExamUpdateAndDelete(APIView):
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
    @swagger_auto_schema(
        operation_description="Retrieve all questions of an exam",
        manual_parameters=[
            openapi.Parameter(
                'exam_id', openapi.IN_PATH, description="ID of the exam", type=openapi.TYPE_STRING
            )
        ],
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
        exam.questions.add(question_id)
        return Response({"message": "Question added to exam"}, status=status.HTTP_200_OK)
