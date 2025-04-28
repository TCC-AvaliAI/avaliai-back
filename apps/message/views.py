from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer, MessageAnswerSerializer
from .models import Message, MessageRole
from .services.get_response_question import get_question_response

class MessageListAndCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all questions",
        responses={200: MessageSerializer(many=True)}
    )
    def get(self, request):
        serializer = MessageSerializer(data=request.GET)
        user = self.request.user
        questions = Message.objects.filter(user=user)
        serializer = MessageSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new question and get an answer",
        request_body=MessageSerializer,
        responses={201: MessageAnswerSerializer}
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, role=MessageRole.USER)
            content = serializer.validated_data.get('content')
            answer = get_question_response(content)
            assistant_message = Message.objects.create(
                user=request.user,
                content=answer,
                role=MessageRole.ASSISTANT,
            )
            return Response(
                {
                    'answer': MessageSerializer(assistant_message).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MessageUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update a question",
        request_body=MessageSerializer,
        responses={200: MessageSerializer}
    )
    def put(self, request, message_id):
        message = get_object_or_404(Message, pk=message_id)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a question",
        responses={204: "Message deleted"}
    )
    def delete(self, request, message_id):
        message = get_object_or_404(Message, pk=message_id)
        message.delete()
        return Response({"message": "Message deleted"}, status=status.HTTP_204_NO_CONTENT)