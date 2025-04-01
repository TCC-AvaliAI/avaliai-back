import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
    TRUE_FALSE = 'TF', 'True/False'
    ESSAY = 'ES', 'Essay'

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    options = ArrayField(models.CharField(max_length=100))
    answer = models.IntegerField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE
    )