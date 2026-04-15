from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    USER_TYPES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
