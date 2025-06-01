from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import TagSerializer
from .models import Tag



class TagListAndCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all tags",
        responses={200: 'List of tags'}
    )
    def get(self, request):
        serializer = TagSerializer(data=request.GET)
        user = self.request.user
        tags = Tag.objects.filter(user=user)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new tag",
        request_body=TagSerializer,
        responses={201: TagSerializer}
    )
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save(user=request.user)
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a tag by ID",
        responses={200: TagSerializer}
    )
    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id, user=request.user)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a tag by ID",
        request_body=TagSerializer,
        responses={200: TagSerializer}
    )
    def put(self, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id, user=request.user)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a tag by ID",
        responses={204: 'No Content'}
    )
    def delete(self, request, tag_id):
        tag = get_object_or_404(Tag, pk=tag_id, user=request.user)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)