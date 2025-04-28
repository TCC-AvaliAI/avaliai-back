from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('user',)

class MessageAnswerSerializer(serializers.Serializer):
    user_message = MessageSerializer()
    assistant_message = MessageSerializer()

