from django.db import models
from Products.models import Boutique
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User

class Gestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None, null=True, blank=True)
    boutique = models.ManyToManyField(
        Boutique,
        blank=True,
        related_name='user_boutique'
    )
    class Meta:
        verbose_name = "Gestionnaire"
        verbose_name_plural = "Gestionnaires"

    def __str__(self):
        return self.user.username
    