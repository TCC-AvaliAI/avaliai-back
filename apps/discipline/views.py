from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discipline
from .serializers import DisciplineSerializer

class DisciplineListAndCreate(APIView):
    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = DisciplineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisciplineUpdateAndDelete(APIView):
    def put(self, request, discipline_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        serializer = DisciplineSerializer(discipline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, discipline_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        discipline.delete()
        return Response({"message": "Discipline deleted"}, status=status.HTTP_204_NO_CONTENT)