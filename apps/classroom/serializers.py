from rest_framework import serializers
from .models import Classroom

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class ClassroomListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)

    class Meta:
        model = Classroom
        fields = ['user']  # Inclua os campos necessários aqui