from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Container(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, related_name='container')