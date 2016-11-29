from rest_framework import serializers
from institution.models import *
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

class LinkSerializer(serializers.ModelSerializer):
    #id = CustomerHyperlink(view_name='service_delete')

    class Meta:
        model = Link
        fields = ['name', 'url', 'institution', 'id']

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'name', 'institution', 'api_link', 'geonode_link']

    def create(self, validated_data):
        obj = Container(**validated_data)
        obj.save()
        return obj

