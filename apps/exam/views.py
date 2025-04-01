from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Exam
from .serializers import ExamSerializer

class ExamListAndCreate(APIView):
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExamUpdateAndDelete(APIView):
    def put(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        serializer = ExamSerializer(exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        exam.delete()
        return Response({"message": "Exam deleted"}, status=status.HTTP_204_NO_CONTENT)