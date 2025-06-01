import uuid
from django.db import models


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
