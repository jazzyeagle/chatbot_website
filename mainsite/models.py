from django.db import models
from login.models import User
from sounds.models import *

# Create your models here.
class Tour(models.Model):
    name       = models.TextField()
    named_by   = models.ForeignKey(User,  on_delete=models.CASCADE)
    month      = models.DateField(unique_for_month=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Venue(models.Model):
    name       = models.TextField()
    named_by   = models.ForeignKey(User,  on_delete=models.CASCADE)
    venue      = models.ForeignKey(Tour,  on_delete=models.CASCADE)
    date       = models.DateField(unique_for_date=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Song(models.Model):
    name       = models.TextField()
    named_by   = models.ForeignKey(User,  on_delete=models.CASCADE)
    venue      = models.ForeignKey(Venue,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sounds     = models.ManyToManyField(Sound, related_name='songs')


class SongRating(models.Model):
    user_id   = models.ForeignKey(User,  on_delete=models.CASCADE)
    song      = models.ForeignKey(Song,  on_delete=models.CASCADE)
    rating    = models.IntegerField()
