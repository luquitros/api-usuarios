from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a default profile when a user is created outside API flow."""
    if created:
        default_type = 'admin' if instance.is_superuser else 'aluno'
        Profile.objects.get_or_create(user=instance, defaults={'user_type': default_type})
