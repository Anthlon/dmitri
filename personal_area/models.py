from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def save(self, *args, **kwargs):
        print('save')
        super().save(*args, **kwargs)

