from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from apps.user.models import User
from .serializers import QuestionSerializer, AIQuestionRequestSerializer, QuestionListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decouple import config
import requests
import json

class QuestionListAndCreate(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all questions",
        request_body=QuestionListSerializer,
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request):
        serializer = QuestionListSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user')
            questions = Question.objects.filter(user=user_id)
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new question",
        request_body=QuestionSerializer,
        responses={201: QuestionSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionUpdateAndDelete(APIView):
    @swagger_auto_schema(
        operation_description="Update a question by ID",
        request_body=QuestionSerializer,
        manual_parameters=[
            openapi.Parameter(
                'question_id', openapi.IN_PATH, description="ID of the question", type=openapi.TYPE_STRING
            )
        ],
        responses={200: QuestionSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a question by ID",
        manual_parameters=[
            openapi.Parameter(
                'question_id', openapi.IN_PATH, description="ID of the question", type=openapi.TYPE_STRING
            )
        ],
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response({"message": "Question deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class CreateQuestionByAI(APIView):
    @swagger_auto_schema(
        operation_description="Create a question using AI",
        request_body=AIQuestionRequestSerializer,
        responses={201: QuestionSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = AIQuestionRequestSerializer(data=request.data)
        api_base = config('AI_API_BASE')

        if serializer.is_valid():
            description = serializer.validated_data['description']
            user_id = serializer.validated_data['user']
            user = get_object_or_404(User, pk=user_id)   
            prompt = f"Generate a question based on the following description: {description}"
            response = requests.post(
                f"{api_base}/api/ai/response/",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"prompt": prompt})
            )
            response_data = response.json()["response"]
            answer = response_data.get('answer')
            if isinstance(answer, str) and answer.isdigit():
                answer = int(answer)

            question = Question.objects.create(
                title=response_data.get('title', ''),
                options=response_data.get('options', []),
                answer=answer if isinstance(answer, int) else None,
                answer_text=response_data.get('answer', ''),
                type=response_data.get('type', ''),
                user=user,
            )
            question.save()

            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
