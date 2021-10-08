from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validate(self, POST):
        errors = {}
        return errors


class User(models.Model):
    username   = models.CharField(max_length=50, unique=True)
    password   = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
