from django.db import models
from users.models import User
from sounds.models import *

# Create your models here.
class Tour(models.Model):
    class Meta:
        app_label = 'mainsite'

    name       = models.TextField()
    url_slug   = models.TextField(blank=True, null=True)
    named_by   = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    month      = models.DateField(unique_for_month=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        named_by = self.named_by.username if self.named_by is not None else ''

        return {
                 'name':       self.name,
                 'named_by':   named_by,
                 'month':      self.month,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class Venue(models.Model):
    class Meta:
        app_label = 'mainsite'

    name       = models.TextField()
    url_slug   = models.TextField(blank=True, null=True)
    named_by   = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    tour       = models.ForeignKey(Tour,  on_delete=models.CASCADE)
    date       = models.DateField(unique_for_date=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def serialize(self):
        named_by = self.named_by.username if self.named_by is not None else ''
        return {
                 'name':        self.name,
                 'named_by':   self.named_by,
                 'tour':       self.tour.serialize(),
                 'date':       self.date,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class VenueSocials(models.Model):
    venue          = models.ForeignKey(Venue, on_delete=models.CASCADE)
    bandcamp       = models.TextField(blank=True, null=True)
    bandcamp_bitly = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class VenueArt(models.Model):
    class Meta:
        app_label = 'mainsite'

    title      = models.TextField()
    artist     = models.CharField(max_length=100)
    year       = models.CharField(max_length=30)
    venue      = models.OneToOneField(Venue, on_delete=models.CASCADE, related_name='cover')
    found_by   = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'title':      self.title,
                 'artist':     self.artist,
                 'year':       self.year,
                 'found_by':   self.found_by.serialize(),
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }


class Song(models.Model):
    class Meta:
        app_label = 'mainsite'

    track_number    = models.IntegerField(blank=True, null=True)
    title           = models.TextField()
    url_slug        = models.TextField(blank=True, null=True)
    named_by        = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name='songs_named')
    commissioned_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='songs_commissioned')
    venue           = models.ForeignKey(Venue,  on_delete=models.CASCADE)
    length          = models.CharField(max_length=10, blank=True, null=True)
    vod_notes       = models.TextField(blank=True, null=True)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def serialize(self):
        requests = []
        for r in self.request_set.all():
            print(r.serialize)
            requests.append(r.serialize())

        named_by = self.named_by.username if self.named_by is not None else ''

        return {
                 'title':       self.title,
                 'named_by':    named_by,
                 'venue':       self.venue.serialize(),
                 'requests':    requests,
                 'created_at':  self.created_at,
                 'updated_at':  self.updated_at
               }


class SongSocials(models.Model):
    song        = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='socials')
    youtube     = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    


class SongRating(models.Model):
    class Meta:
        app_label = 'mainsite'

    user       = models.ForeignKey(User,  on_delete=models.CASCADE)
    song       = models.ForeignKey(Song,  on_delete=models.CASCADE)
    rating     = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'user':       self.user.serialize(),
                 'song':       self.song.serialize(),
                 'rating':     self.rating,
                 'created_at': self.created_at
               }
