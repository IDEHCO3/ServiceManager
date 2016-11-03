from rest_framework import serializers
from institution.models import InstitutionProfile, Container, Service
from rest_framework.reverse import reverse


class CustomerHyperlink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'institution_initials': obj.institution.initials,
            'pk': obj.id
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

class InstitutionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionProfile
        fields = ['name', 'initials', 'description', 'image', 'user']

class ServiceSerializer(serializers.ModelSerializer):
    #id = CustomerHyperlink(view_name='service_delete')

    class Meta:
        model = Service
        fields = ['url', 'institution', 'id']

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['name', 'folderOfDatabase', 'institution']

