from rest_framework import serializers
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    class Meta:
        model = Exam
        fields = ['user']