from django.db import models
from login.models import User

# Create your models here.
class Category(models.Model):
    text       = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubCategory(models.Model):
    text       = models.CharField(max_length=255)
    category   = models.ForeignKey(Category,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sound(models.Model):
    code        = models.CharField(max_length=3)
    name        = models.TextField()
    renamed_by  = models.ForeignKey(User,  on_delete=models.CASCADE)
    category    = models.ForeignKey(Category,  on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,  on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class SoundRating(models.Model):
    user       = models.ForeignKey(User,  on_delete=models.CASCADE)
    sound      = models.ForeignKey(Sound,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Instrument(models.Model):
    code        = models.CharField(max_length=3)
    name        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
