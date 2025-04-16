from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Exam
from .serializers import ExamSerializer, ExamListSerializer, ExamStatisticsSerializer
from apps.question.serializers import QuestionSerializer
from apps.question.models import Question
from avaliai.ai_prompt import AIPrompt
from decouple import config
import requests
import json
from django.core.exceptions import ValidationError
from .services.exam_statistics import get_exam_statistics

class ExamListAndCreate(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all exams",
        query_serializer=ExamListSerializer,
        responses={
            200: ExamSerializer(many=True),
            400: "Bad Request - UUID inválido"
        }
    )
    def get(self, request):
        serializer = ExamListSerializer(data=request.GET)
        try:
            if serializer.is_valid():
                user_id = serializer.validated_data.get('user')
                exams = Exam.objects.filter(user=user_id)
                serializer = ExamSerializer(exams, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "UUID de usuário inválido", "details": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {"error": "UUID de usuário inválido", "details": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Erro ao buscar exames", "details": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
class ExamDetailUpdateAndDelete(APIView):
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
        exam.questions.add(question_id)
        return Response({"message": "Question added to exam"}, status=status.HTTP_200_OK)

class CreateExamByAI(APIView):
    @swagger_auto_schema(
        operation_description="Create a new exam and generate questions using AI",
        request_body=ExamSerializer,
        responses={201: ExamSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        api_base = config('AI_API_BASE')
        
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
                response = requests.post(
                    f"{api_base}/api/ai/response/",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"prompt": prompt})
                )
                response_data = response.json()
                exam = serializer.save(was_generated_by_ai=True)
                for question_data in response_data["response"]:
                    answer = question_data['answer']
                    if isinstance(answer, str) and answer.isdigit():
                        answer = int(answer)
                    question = Question.objects.create(
                        title=question_data['title'],
                        options=question_data['options'],
                        answer=answer if isinstance(answer, int) else None,
                        answer_text=question_data['answer'],
                        type=question_data['type'],
                        user=data.get('user'),
                    )
                    question.save()
                    exam.questions.add(question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExamDetails(APIView):
    def get(self, request):
        stats = get_exam_statistics()
        serializer = ExamStatisticsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)