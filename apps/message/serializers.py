from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    model = serializers.CharField(write_only=True, required=True)
    api_key = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Message
        exclude = ('user',)

    def create(self, validated_data):
        validated_data.pop('model', None)
        validated_data.pop('api_key', None)
        return super().create(validated_data)

class MessageAnswerSerializer(serializers.Serializer):
    user_message = MessageSerializer()
    assistant_message = MessageSerializer()

