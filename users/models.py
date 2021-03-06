from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validate(self, POST):
        errors = {}
        return errors


class User(models.Model):
    class Meta:
        app_label = 'users'

    username   = models.CharField(max_length=50, unique=True)
    email      = models.CharField(max_length=255)
    saymyname  = models.TextField(null=True, blank=True)
    password   = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The serialized data will not include the password.  Login will not
    #     be handled via JavaScript.
    def serialize(self):
        return {
                 'username':   self.username,
                 'saymyname':  self.saymyname,
                 'created_at': self.created_at,
                 'updated_at': self.updated_at
               }

class UserPronoun(models.Model):
    class Meta:
        app_label = 'users'
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    subjective = models.CharField(max_length=10)
    objective  = models.CharField(max_length=10)
    possessive = models.CharField(max_length=10)
