"""Defines singals."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from playstyle_compass.models import UserPreferences
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_models(sender, instance, created, **kwargs):
    """Create user models."""
    if created:
        if instance.is_superuser:
            user_profile = UserProfile.objects.create(user=instance)
            user_profile.profile_name = "admin"
            user_profile.save()
        UserPreferences.objects.create(user=instance)


post_save.connect(create_user_models, sender=User)
