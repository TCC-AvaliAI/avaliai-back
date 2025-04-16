from rest_framework import serializers
from .models import Exam
from apps.question.models import Question
from apps.question.serializers import QuestionSerializer
import uuid

class SimpleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    questions = SimpleQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['discipline'] = instance.discipline.name
        representation['classroom'] = instance.classroom.name
        return representation

class ExamListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    
    def validate_user(self, value):
        if value == 'undefined' or not value:
            raise serializers.ValidationError("É necessário um UUID de usuário válido")
        try:
            return str(uuid.UUID(value))
        except ValueError:
            raise serializers.ValidationError("UUID de usuário inválido")
    
    class Meta:
        model = Exam
        fields = ['user']


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