from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from apps.user.models import User
from .serializers import QuestionSerializer, AIQuestionRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decouple import config
from django.utils import timezone
import requests
import json
from rest_framework.pagination import PageNumberPagination

class QuestionListAndCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all questions",
        query_serializer=QuestionSerializer,
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request):
        serializer = QuestionSerializer(data=request.GET)
        user = self.request.user
        questions = Question.objects.filter(user=user)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    @swagger_auto_schema(
        operation_description="Create a new question",
        request_body=QuestionSerializer,
        responses={201: QuestionSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
            user = self.request.user 
            prompt = f"Generate a question based on the following description: {description}"
            try:
                response = requests.post(
                    f"{api_base}/api/ai/response/",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"prompt": prompt})
                )
                if response.status_code != 200:
                    return Response(
                        {"error": f"AI API returned an error: {response.status_code}"},
                        status=status.HTTP_502_BAD_GATEWAY
                    )
                response_data = response.json().get("response", {})
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Failed to connect to AI API: {str(e)}"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON response from AI API"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            answer = response_data.get('answer')
            if isinstance(answer, str) and answer.isdigit():
                answer = int(answer)

            question = Question.objects.create(
                title=response_data.get('title', ''),
                options=response_data.get('options', []),
                answer=answer if isinstance(answer, int) else None,
                answer_text=response_data.get('answer', ''),
                type=response_data.get('type', ''),
                user=request.user,  # Adicionando o usuário aqui
            )
            question.save()

            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecentQuestions(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve recent questions with pagination",
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request):
        user = self.request.user
        current_date = timezone.now().month
        questions = Question.objects.filter(user=user, created_at__month=current_date).order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_questions = paginator.paginate_queryset(questions, request)
        
        serializer = QuestionSerializer(paginated_questions, many=True)
        return paginator.get_paginated_response(serializer.data)