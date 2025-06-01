from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AIQuestionRequestSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    model = serializers.CharField(required=True, help_text="Model to use for AI generation")
    api_key = serializers.CharField(required=False,allow_blank=True, help_text="API key for the AI service")

    class Meta:
        fields = ('description', 'model', 'api_key')

class NestedTagSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100, required=False)


class QuestionWithTagsSerializer(serializers.ModelSerializer):
    tags = NestedTagSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('tags',)