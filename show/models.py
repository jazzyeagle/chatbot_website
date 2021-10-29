from django.db       import models
from users.models    import User
from mainsite.models import *
from sounds.models   import *


class RequestType(models.Model):
    class Meta:
        app_label = 'show'

    text          = models.CharField(max_length=50)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
                 'text':          self.text,
                 'created_at':    self.created_at,
                 'updated_at':    self.updated_at
               }


class Request(models.Model):
    class Meta:
        app_label = 'show'

    request_type  = models.ForeignKey(RequestType, on_delete=models.CASCADE)
    played_by     = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='played_by')
    requested_by  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='requested_by')
    text          = models.CharField(max_length=255, blank=True, null=True)
    sound         = models.ForeignKey(Sound, on_delete=models.CASCADE, blank=True, null=True)
    instrument    = models.ForeignKey(Instrument, on_delete=models.CASCADE, blank=True, null=True)
    used_on_track = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def serialize(self):
        requested_by  = self.requested_by.username       if self.requested_by  is not None else ''
        played_by     = self.played_by.username          if self.played_by     is not None else ''
        sound         = self.sound.serialize()           if self.sound         is not None else ''
        instrument    = self.sound.serialize()           if self.sound         is not None else ''
        used_on_track = self.used_on_track.title         if self.used_on_track is not None else ''

        return {
                 'requested_by':  requested_by,
                 'played_by':     played_by,
                 'text':          self.text,
                 'sound':         sound,
                 'instrument':    instrument,
                 'used_on_track': used_on_track,
                 'created_at':    self.created_at,
                 'updated_at':    self.updated_at
               }
