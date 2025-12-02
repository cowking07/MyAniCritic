from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    This should be called whenever a user is created or saved.
    The purpose is to create a UserProfile object for each created user.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()