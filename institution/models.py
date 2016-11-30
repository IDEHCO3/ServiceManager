from django.db import models
from django.contrib.auth.models import User

import os
import shutil
import docker
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

class Container(models.Model):
    containers = "containers"
    base_port = 8000
    containers_prefix = "serviceManager."
    host = "ecoide.org"
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    institution = models.OneToOneField(InstitutionProfile, related_name='container')

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

    @property
    def api_port(self):
        if self.id is None:
            return None
        return (self.id*2)+Container.base_port

    @property
    def geonode_port(self):
        if self.id is None:
            return None
        return (self.id*2)+Container.base_port+1

    @property
    def api_link(self):
        if self.id is None:
            return None
        return "http://"+Container.host+":"+str(self.api_port)+"/"

    @property
    def geonode_link(self):
        if self.id is None:
            return None
        return "http://"+Container.host+":"+str(self.geonode_port)+"/"

    def get_container_base_name(self):
        if self.id is None:
            return None
        return Container.containers_prefix+str(self.id)

    @property
    def api_container_name(self):
        return self.get_container_base_name()+"_api"

    @property
    def geonode_container_name(self):
        return self.get_container_base_name()+"_geonode"

    @property
    def api_container_db_name(self):
        return self.get_container_base_name()+"_database_api"

    @property
    def geonode_container_db_name(self):
        return self.get_container_base_name()+"_database_api"

    def create_folders(self):
        if not os.path.exists(os.getcwd()+"/"+Container.containers):
            os.mkdir(os.getcwd()+"/"+Container.containers)

        if self.container_folder is not None and not os.path.exists(self.container_folder):
            os.mkdir(self.container_folder)
        if self.geonode_folder is not None and not os.path.exists(self.geonode_folder):
            os.mkdir(self.geonode_folder)
        if self.api_folder is not None and not os.path.exists(self.api_folder):
            os.mkdir(self.api_folder)

    def connectInDocker(self):
        tls_config = docker.tls.TLSConfig(ca_cert='CA/ca.pem', client_cert=('CA/cert.pem', 'CA/key.pem'))
        cli = docker.Client(base_url='tcp://172.17.0.1:2376', tls=tls_config)
        #cli = docker.Client(base_url='unix://var/run/docker.sock')
        return cli

    def create_container(self, image, port, database_ip, name):
        cli = self.connectInDocker()
        container = cli.create_container(
            image=image,
            name=name,
            ports=[80],
            environment={"DB_IP": database_ip},
            host_config=cli.create_host_config(
                port_bindings={
                    80: port,
                },
                dns=['146.164.34.2']))
        cli.start(container=container.get('Id'))

    def create_database_container(self, database_folder, name):
        cli = self.connectInDocker()
        container = cli.create_container(
            image="database",
            name=name,
            ports=[5432],
            host_config=cli.create_host_config(
                binds=[database_folder+':/var/lib/postgresql/data'],
                dns=['146.164.34.2']))
        cli.start(container=container.get('Id'))
        ip = cli.inspect_container(container.get('Id'))['NetworkSettings']['Networks']['bridge']['IPAddress']
        return ip

    def create_containers(self):
        self.create_folders()
        database_ip = self.create_database_container(self.api_folder, self.api_container_db_name)
        self.create_container("idehco3_base", self.api_port, database_ip, self.api_container_name)
        #database_ip = self.create_database_container(self.geonode_folder, self.geonode_container_db_name)
        #self.create_container("geonode", self.api_port, database_ip, self.geonode_container_name)


    def delete_containers(self):
        cli = self.connectInDocker()
        containers = [
            self.api_container_name,
            self.api_container_db_name,
            self.geonode_container_name,
            self.geonode_container_db_name
        ]

        for container in containers:
            if container is None:
                continue
            try:
                cli.stop(container=container)
                cli.remove_container(container=container)
            except:
                continue

        if self.container_folder is not None and os.path.exists(self.container_folder):
            shutil.rmtree(self.container_folder)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Container, self).save(force_insert, force_update, using, update_fields)
        self.create_containers()

    def delete(self, using=None):
        self.delete_containers()
        super(Container, self).delete(using)

    def start_api(self):
        if self.id is not None:
            cli = self.connectInDocker()
            cli.start(container=self.api_container_name)

    def stop_api(self):
        if self.id is not None:
            cli = self.connectInDocker()
            cli.stop(container=self.api_container_name)

    def start_geonode(self):
        if self.id is not None:
            cli = self.connectInDocker()
            cli.start(container=self.geonode_container_name)

    def stop_geonode(self):
        if self.id is not None:
            cli = self.connectInDocker()
            cli.stop(container=self.geonode_container_name)
