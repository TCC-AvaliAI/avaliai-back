import uuid
from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identification = models.CharField(max_length=255)
    usual_name = models.CharField(max_length=255)
    avatar = models.URLField(max_length=255)
    role = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
            
    def assign_group(self):
        groups = {
            'Professor': 'teacher',
            'Aluno': 'student',
        }
        group_name = groups.get(self.role)
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                self.groups.add(group)
            except Group.DoesNotExist:
                print(f'Group {group_name} does not exist')

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    if not kwargs['created']:
        instance.assign_group()
