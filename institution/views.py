from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response

import json
import requests

from institution.serializers import *
from institution.models import *

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
    serializer_class = LinkSerializer

    def makeRequest(self, request):
        response_from_api = requests.options(request.data['url'])
        if response_from_api.status_code == 200:
            return response_from_api
        return None


    def getServices(self, response):
        services = {}
        jsonld = json.loads(response.content)
        if '@context' in jsonld:
            for key in jsonld['@context']:
                attr = jsonld['@context'][key]
                if isinstance(attr, dict) and attr['@type'] == '@id' and key in jsonld:
                    services[key] = jsonld[key]
        return services

    def saveServices(self, response, services):
        if response.status_code == 201:
            id = response.data['id']
            link = Link.objects.get(id=id)
            for key in services:
                Service(name=key, url=services[key], link=link).save()


    def post(self, request, *args, **kwargs):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        request.data['institution'] = institution.id

        #response_from_api = self.makeRequest(request)
        #if response_from_api is None:
        #    return Response(data={'Error': "The system can't find the services of this link"}, status=404)
        #services = self.getServices(response_from_api)
        response = super(LinkListByInstitution, self).post(request, *args, **kwargs)
        #self.saveServices(response, services)
        return response

    def get_queryset(self):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        self.queryset = institution.links.all()
        return self.queryset

class LinkDeleteByInstitution(generics.DestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

# class ServiceList(generics.ListAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#
#     def get_queryset(self):
#         queryset = self.queryset
#         if 'institution_initials' in self.kwargs:
#             queryset = queryset.filter(link__institution__initials=self.kwargs.get('institution_initials'))
#
#         if 'link_id' in self.kwargs:
#             queryset = queryset.filter(link=self.kwargs.get('link_id'))
#
#         if 'search' in self.request.query_params:
#             search = self.request.query_params.get('search')
#             queryset = queryset.filter(name__icontains=search)
#
#         return queryset

class ContainerCreate(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerDetail(generics.RetrieveDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

