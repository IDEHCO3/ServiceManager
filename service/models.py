from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    url = models.CharField(max_length=1000, null=False, blank=False)
    user = models.ForeignKey(User, related_name='srevices')