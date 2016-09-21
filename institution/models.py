from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class InstitutionProfile(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False)
    initials = models.CharField(max_length=255, null=True, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=False)
    image = models.ImageField(upload_to='images/institutions/', null=True, blank=False)
    user = models.OneToOneField(User, related_name='institution_profile')

class Service(models.Model):
    url = models.CharField(max_length=1000, null=False, blank=False)
    institution = models.ForeignKey(InstitutionProfile, related_name='services')

class Container(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    institution = models.ForeignKey(InstitutionProfile, related_name='container')

    @property
    def name_api(self):
        return self.name + "_api"

    @property
    def name_geonode(self):
        return self.name + "_geonode"