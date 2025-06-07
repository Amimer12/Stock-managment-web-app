from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Gestionnaire


@receiver(post_delete, sender=Gestionnaire)
def delete_user_with_gestionnaire(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()