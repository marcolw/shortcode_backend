from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from authentication.models import User
from .operations import sync_user_column_profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print ('created user')
        column_profile = models.ColumnProfile.objects.create(user=instance, description="Default")
        sync_user_column_profile(instance)
        models.UserSetting.objects.create(user=instance, active_column_profile=column_profile)
