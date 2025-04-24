from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AIQuestionRequestSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    user = serializers.CharField(required=True)
