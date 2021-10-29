from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    class Meta:
        app_label = 'sounds'

    text       = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'text':       self.text,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class SubCategory(models.Model):
    class Meta:
        app_label = 'sounds'

    text       = models.CharField(max_length=255)
    category   = models.ForeignKey(Category,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'text':       self.text,
                 'category':   self.category.serialize(),
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class Sound(models.Model):
    class Meta:
        app_label = 'sounds'

    code        = models.CharField(max_length=3)
    name        = models.TextField()
    renamed_by  = models.ForeignKey(User,  on_delete=models.CASCADE, null=True, blank=True)
    category    = models.ForeignKey(Category,  on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,  on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def serialize(self):
        renamed_by = self.renamed_by if self.renamed_by is not None else ''

        return {
                 'code':        self.code,
                 'name':        self.name,
                 'renamed_by':  renamed_by,
                 'category':    self.category.text,
                 'subcategory': self.subcategory.text,
                 'created_at':  self.created_at,
                 'updated_at':  self.updated_at
               }


class SoundRating(models.Model):
    class Meta:
        app_label = 'sounds'

    user       = models.ForeignKey(User,  related_name='ratings', on_delete=models.CASCADE)
    sound      = models.ForeignKey(Sound, related_name='ratings', on_delete=models.CASCADE)
    rating     = models.IntegerField(null=True, blank=True)  # Null/Blank allowed based on rating being added after created.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'user':       self.user.serialize(),
                 'sound':      self.sound.serialize(),
                 'rating':     self.rating,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class Instrument(models.Model):
    class Meta:
        app_label = 'sounds'

    code         = models.CharField(max_length=3, blank=True, null=True)
    name         = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'code':       self.code,
                 'name':       self.name,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }
