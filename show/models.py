from django.db       import models
from login.models    import User
from mainsite.models import *
from sounds.models   import *


# Create your models here.
class Request(models.Model):
    class Meta:
        app_label = 'show'
    user         = models.ForeignKey(User,  on_delete=models.CASCADE)
    sound        = models.ForeignKey(Sound,  on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
