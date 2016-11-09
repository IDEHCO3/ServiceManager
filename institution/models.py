from django.db import models
from django.contrib.auth.models import User

import os
import shutil
# Create your models here.

class InstitutionProfile(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False)
    initials = models.CharField(max_length=255, null=True, blank=False, unique=True)
    description = models.CharField(max_length=2000, null=True, blank=False)
    image = models.ImageField(upload_to='images/institutions/', null=True, blank=False)
    user = models.OneToOneField(User, related_name='institution_profile')

class Link(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=1000, null=False, blank=False)
    institution = models.ForeignKey(InstitutionProfile, related_name='links')

# class Service(models.Model):
#     name = models.CharField(max_length=255, null=False, blank=False)
#     url = models.CharField(max_length=1000, null=False, blank=False)
#     link = models.ForeignKey(Link, related_name='services')

class Container(models.Model):
    containers = "containers"
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    institution = models.ForeignKey(InstitutionProfile, related_name='container')

    @property
    def name_api(self):
        return self.name + "_api"

    @property
    def name_geonode(self):
        return self.name + "_geonode"

    @property
    def container_folder(self):
        if self.id is not None:
            return os.getcwd()+"/"+Container.containers+"/"+str(self.id)
        else:
            return None

    @property
    def geonode_folder(self):
        if self.container_folder is not None:
            return self.container_folder+"/geonode"
        else:
            return None

    @property
    def api_folder(self):
        if self.container_folder is not None:
            return self.container_folder+"/api"
        else:
            return None

    def create_folders(self):
        if not os.path.exists(os.getcwd()+"/"+Container.containers):
            os.mkdir(os.getcwd()+"/"+Container.containers)

        if self.container_folder is not None and not os.path.exists(self.container_folder):
            os.mkdir(self.container_folder)
        if self.geonode_folder is not None and not os.path.exists(self.geonode_folder):
            os.mkdir(self.geonode_folder)
        if self.api_folder is not None and not os.path.exists(self.api_folder):
            os.mkdir(self.api_folder)


    def create_containers(self):
        self.create_folders()

    def delete_containers(self):
        if self.container_folder is not None and os.path.exists(self.container_folder):
            shutil.rmtree(self.container_folder)

    def save(self):
        super(Container, self).save()
        self.create_containers()

    def delete(self):
        self.delete_containers()
        super(Container, self).delete()