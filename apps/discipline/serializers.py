from rest_framework import serializers
from .models import Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        exclude = ('user',)
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class DisciplineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = []