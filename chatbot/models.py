from django.db import models
from mainsite.models import User


class Command(models.Model):
    class Meta:
        app_label = 'chatbot'

    name       = models.TextField(unique=True)
    script     = models.TextField()
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name='original_commands')
    updated_by = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name='updated_commands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Variable(models.Model):
    class Meta:
        app_label = 'chatbot'

    name       = models.TextField()
    value      = models.TextField()
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name='original_variables')
    updated_by = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name='updated_variables')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConnectionSetting(models.Model):
    class meta:
        app_label = 'chatbot'

    platform   = models.TextField()
    field      = models.TextField()
    value      = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
