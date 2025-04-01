from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discipline
from .serializers import DisciplineSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DisciplineListAndCreate(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all disciplines",
        responses={200: DisciplineSerializer(many=True)}
    )
    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new discipline",
        request_body=DisciplineSerializer,
        responses={201: DisciplineSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = DisciplineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DisciplineUpdateAndDelete(APIView):
    @swagger_auto_schema(
        operation_description="Update a discipline by ID",
        request_body=DisciplineSerializer,
        manual_parameters=[
            openapi.Parameter(
                'discipline_id', openapi.IN_PATH, description="ID of the discipline", type=openapi.TYPE_STRING
            )
        ],
        responses={200: DisciplineSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, discipline_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        serializer = DisciplineSerializer(discipline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a discipline by ID",
        manual_parameters=[
            openapi.Parameter(
                'discipline_id', openapi.IN_PATH, description="ID of the discipline", type=openapi.TYPE_STRING
            )
        ],
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, discipline_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        discipline.delete()
        return Response({"message": "Discipline deleted"}, status=status.HTTP_204_NO_CONTENT)