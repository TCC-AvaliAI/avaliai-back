from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "apps.user":
        for group_name in ["teacher", "student"]:
            Group.objects.get_or_create(name=group_name)
