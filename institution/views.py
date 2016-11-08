from rest_framework import generics
from rest_framework.views import APIView
from institution.models import InstitutionProfile, Link, Container
from institution.serializers import InstitutionProfileSerializer, ServiceSerializer, ContainerSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response

import json
import requests

class InstitutionList(generics.ListAPIView):
    queryset = InstitutionProfile.objects.all()
    serializer_class = InstitutionProfileSerializer

class InstitutionDetail(generics.RetrieveAPIView):
    queryset = InstitutionProfile.objects.all()
    serializer_class = InstitutionProfileSerializer

    lookup_field = "initials"
    lookup_url_kwarg = "initials"

class ProfileDetail(APIView):

    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        institution = request.user.institution_profile
        institution_serializer = InstitutionProfileSerializer(institution)
        response = Response(institution_serializer.data)
        return response


class LinkListByInstitution(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = ServiceSerializer

    def getLayers(self, layers_jsonld):
        jsonld = json.loads(layers_jsonld)
        layers = {}
        for key in jsonld['@context']:
            attr = jsonld['@context'][key]
            if attr['@type'] == '':
                layers[key] = jsonld[key]
        return layers

    def post(self, request, *args, **kwargs):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        request.data['institution'] = institution.id
        response_from_api = requests.options(request.data['url'])
        if response_from_api.status_code == 200:
            layers = self.getLayers(response_from_api.content)
        else:
            layers = None
        response = super(LinkListByInstitution, self).post(request, *args, **kwargs)
        return response

    def get_queryset(self):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        self.queryset = institution.services.all()
        return self.queryset

class LinkDeleteByInstitution(generics.DestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = ServiceSerializer

class ContainerCreate(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerDetail(generics.RetrieveDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

