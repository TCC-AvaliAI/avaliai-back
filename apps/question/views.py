from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question
from .serializers import QuestionSerializer, AIQuestionRequestSerializer, QuestionWithTagsSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from .services.create_question_by_ai import QuestionService

class QuestionListAndCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all questions",
        query_serializer=QuestionSerializer,
        responses={200: QuestionSerializer(many=True)}
    )
    def get(self, request):
        serializer = QuestionSerializer(data=request.GET)
        questions = Question.objects.all().select_related("user").prefetch_related("tags").order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_questions = paginator.paginate_queryset(questions, request)
        serializer = QuestionSerializer(paginated_questions, many=True)
        return paginator.get_paginated_response(serializer.data)
       
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
        if serializer.is_valid():
            question = QuestionService.create_question(serializer, request)
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
    
class QuestionListAndAddTags(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a question with its tags",
        responses={200: QuestionWithTagsSerializer()}
    )
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionWithTagsSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Add tags to a question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="Array of tag IDs"
                )
            },
            required=['tags']
        ),
        responses={200: QuestionWithTagsSerializer()}
    )
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        tags = request.data.get('tags', [])     
        if not tags:
            return Response(
                {"error": "Provide at least one tag"}, 
                status=status.HTTP_400_BAD_REQUEST
            )  
        try:
            all_tags = list(question.tags.all().values_list("id", flat=True))
            concact_tags = tags + all_tags
            question.tags.set(concact_tags) 
            serializer = QuestionWithTagsSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @swagger_auto_schema(
        operation_description="Remove a tag from a question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tag_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID of the tag to remove"
                )
            },
            required=['tag_id']
        ),
        responses={
            204: "No Content",
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        tag_id = request.data.get('tag_id')
        
        if tag_id is None:
            return Response(
                {"error": "tag_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not question.tags.filter(id=tag_id).exists():
            return Response(
                {"error": "Tag not found for this question"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        question.tags.remove(tag_id)
        return Response(status=status.HTTP_204_NO_CONTENT)