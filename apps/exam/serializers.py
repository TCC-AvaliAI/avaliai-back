from rest_framework import serializers
from .models import Exam
from apps.question.models import Question
from apps.question.serializers import QuestionSerializer
import uuid

class SimpleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('user',)

class ExamSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    questions = SimpleQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        exclude = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['discipline'] = instance.discipline.name
        representation['classroom'] = instance.classroom.name
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
    recent_questions = QuestionSerializer(many=True)

class UpdateExamQRCodeSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField(required=True)
    class Meta:
        model = Exam
        fields = ['qr_code']