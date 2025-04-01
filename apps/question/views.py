from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class QuestionListAndCreate(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all questions",
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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