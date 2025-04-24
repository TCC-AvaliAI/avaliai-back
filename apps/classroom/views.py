from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Classroom
from .serializers import ClassroomSerializer, ClassroomListSerializer

class ClassroomListAndCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all classrooms",
        query_serializer=ClassroomListSerializer,
        responses={200: ClassroomSerializer(many=True)}
    )
    def get(self, request):
        serializer = ClassroomListSerializer(data=request.GET)
        user = self.request.user
        classrooms = Classroom.objects.filter(user=user)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new classroom",
        request_body=ClassroomSerializer,
        responses={201: ClassroomSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClassroomUpdateAndDelete(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update a classroom by ID",
        request_body=ClassroomSerializer,
        manual_parameters=[
            openapi.Parameter(
                'classroom_id', openapi.IN_PATH, description="ID of the classroom", type=openapi.TYPE_STRING
            )
        ],
        responses={200: ClassroomSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, classroom_id):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a classroom by ID",
        manual_parameters=[
            openapi.Parameter(
                'classroom_id', openapi.IN_PATH, description="ID of the classroom", type=openapi.TYPE_STRING
            )
        ],
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, classroom_id):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        classroom.delete()
        return Response({"message": "Classroom deleted"}, status=status.HTTP_204_NO_CONTENT)