import uuid
from django.db import models

class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
