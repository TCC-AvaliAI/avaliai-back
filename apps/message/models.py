import uuid
from django.db import models


class MessageRole(models.TextChoices):
    ASSISTANT = 'assistant', 'Assistente'
    USER = 'user', 'Usuário'

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=MessageRole.choices,
        default=MessageRole.USER,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)