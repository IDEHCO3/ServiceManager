from rest_framework import serializers
from institution.models import InstitutionProfile, Container, Service


class InstitutionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionProfile
        fields = ['name', 'initials', 'description', 'image', 'user']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['url', 'institution']

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['name', 'folderOfDatabase', 'institution']

