from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Classroom
from .serializers import ClassroomSerializer

class ClassroomListAndCreate(APIView):
    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClassroomUpdateAndDelete(APIView):
    def put(self, request, classroom_id):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, classroom_id):
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        classroom.delete()
        return Response({"message": "Classroom deleted"}, status=status.HTTP_204_NO_CONTENT)