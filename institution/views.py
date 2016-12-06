from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response

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

    def post(self, request, *args, **kwargs):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        request.data['institution'] = institution.id
        response = super(LinkListByInstitution, self).post(request, *args, **kwargs)
        return response

    def get_queryset(self):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        self.queryset = institution.links.all()
        return self.queryset

class LinkDeleteByInstitution(generics.DestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ContainerList(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

    def post(self, request, *args, **kwargs):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        request.data['institution'] = institution.id
        response = super(ContainerList, self).post(request, *args, **kwargs)
        return response

class ContainerDetail(generics.RetrieveDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerControls(APIView):

    def get(self, request, *args, **kwargs): # return the status of container
        if 'container' in kwargs:
            initials = kwargs.get('institution_initials')
            institution = InstitutionProfile.objects.get(initials=initials)
            container = institution.container
            data = {"status": "unknow"}
            if kwargs.get('container').lower() == 'api':
                data = container.get_api_status()

            if kwargs.get('container').lower() == 'geonode':
                data = container.get_geonode_status()

            return Response(data, status=200)
        else:
            return Response({"Error": "page not found!"}, status=404)

    def post(self, request, *args, **kwargs): # start the container
        if 'container' in kwargs:
            initials = kwargs.get('institution_initials')
            institution = InstitutionProfile.objects.get(initials=initials)
            container = institution.container
            data = {"status": "unknow"}
            if kwargs.get('container').lower() == 'api':
                container.start_api()
                data = container.get_api_status()

            if kwargs.get('container').lower() == 'geonode':
                container.start_geonode()
                data = container.get_geonode_status()

            return Response(data, status=200)
        else:
            return Response({"Error": "page not found!"}, status=404)

    def delete(self, request, *args, **kwargs): # stop the container
        if 'container' in kwargs:
            initials = kwargs.get('institution_initials')
            institution = InstitutionProfile.objects.get(initials=initials)
            container = institution.container
            data = {"status": "unknow"}
            if kwargs.get('container').lower() == 'api':
                container.stop_api()
                data = container.get_api_status()

            if kwargs.get('container').lower() == 'geonode':
                container.stop_geonode()
                data = container.get_geonode_status()

            return Response(data, status=200)
        else:
            return Response({"Error": "page not found!"}, status=404)
