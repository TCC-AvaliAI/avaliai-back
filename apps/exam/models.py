import uuid
from django.db import models

class ExamStatus(models.TextChoices):
    APPLIED = 'APPLIED', 'Aplicada'
    PENDING = 'PENDING', 'Pendente'
    CANCELLED = 'CANCELLED', 'Cancelada'
    ARCHIVED = 'ARCHIVED', 'Arquivada'

class ExamDifficulty(models.TextChoices):
    EASY = 'EASY', 'Fácil'
    MEDIUM = 'MEDIUM', 'Média'
    HARD = 'HARD', 'Difícil'

class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    discipline = models.ForeignKey('discipline.Discipline', on_delete=models.CASCADE)
    classroom = models.ForeignKey('classroom.Classroom', on_delete=models.CASCADE)
    duration = models.IntegerField(blank=True, default=0)
    score = models.IntegerField(blank=True, default=0)
    questions = models.ManyToManyField('question.Question', blank=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(blank=True, null=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=1000)
    theme = models.CharField(max_length=255)
    was_generated_by_ai = models.BooleanField(default=False)
    difficulty = models.CharField(
        max_length=20,
        choices=ExamDifficulty.choices,
        default=ExamDifficulty.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=ExamStatus.choices,
        default=ExamStatus.PENDING
    )