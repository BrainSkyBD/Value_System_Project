from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib


class User(AbstractUser):
    phone_number = models.CharField(max_length=255, default='', blank=True, null=True)
    User_Role_Option = (
        ('Admin', 'Admin'),
        ('manager', 'manager'),
        ('Viewer', 'Viewer'),
    )
    User_Role = models.CharField(max_length=255, choices=User_Role_Option, default='Admin')
    # Self-referencing ForeignKey for 'created_by'
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    # Automatically store the time when the user is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username