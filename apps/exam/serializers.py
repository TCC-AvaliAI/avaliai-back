from rest_framework import serializers
from .models import Exam
from apps.question.models import QuestionType
from apps.discipline.serializers import DisciplineSerializer
from apps.classroom.serializers import ClassroomSerializer
from apps.tag.serializers import TagSerializer

class NestedQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=500)
    options = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    answer = serializers.IntegerField(required=False)
    answer_text = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=QuestionType.choices)
    score = serializers.IntegerField(default=0)
    was_generated_by_ai = serializers.BooleanField(default=False)
    tags = TagSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ExamSerializer(serializers.ModelSerializer):
    questions = NestedQuestionSerializer(many=True, required=False)
    model = serializers.CharField(required=False, help_text="Model to use for AI generation")
    api_key = serializers.CharField(required=False, allow_blank=True, help_text="API key for the AI service")
    class Meta:
        model = Exam
        exclude = ('user',)

    def create(self, validated_data):
        validated_data.pop('model', None)
        validated_data.pop('api_key', None)
        questions_data = validated_data.pop('questions', None)
        validated_data['user'] = self.context['request'].user
        exam = Exam.objects.create(**validated_data)
        
        if questions_data:
            from apps.question.models import Question
            for question_data in questions_data:
                
                question = Question.objects.create(
                    user=self.context['request'].user,
                    **question_data
                )
                exam.questions.add(question)
        
        return exam

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['discipline'] = DisciplineSerializer(instance.discipline).data
        representation["classroom"] = ClassroomSerializer(instance.classroom).data
        representation['status'] = instance.get_status_display()  
        representation['difficulty'] = instance.get_difficulty_display()
        return representation

class ExamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = []

class ExamStatisticsSerializer(serializers.Serializer):
    total_exams = serializers.IntegerField()
    last_month = serializers.IntegerField()
    total_weeks = serializers.IntegerField()
    last_week = serializers.IntegerField()
    applied_last_month= serializers.IntegerField()
    total_questions = serializers.IntegerField()
    total_questions_last_month = serializers.IntegerField()
    total_exams_applied = serializers.IntegerField()
    total_exams_generated_by_ai = serializers.IntegerField()
    total_exams_generated_by_ai_last_month = serializers.IntegerField()
    recent_exams = ExamSerializer(many=True)
class UpdateExamQRCodeSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField(required=True)
    class Meta:
        model = Exam
        fields = ['qr_code']