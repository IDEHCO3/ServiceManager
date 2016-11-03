from rest_framework import generics
from rest_framework.views import APIView
from institution.models import InstitutionProfile, Service, Container
from institution.serializers import InstitutionProfileSerializer, ServiceSerializer, ContainerSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response

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


class ServiceListByInstitution(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def post(self, request, *args, **kwargs):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        request.data['institution'] = institution.id
        response = super(ServiceListByInstitution, self).post(request, *args, **kwargs)
        return response

    def get_queryset(self):
        institution_initials = self.kwargs.get('institution_initials', None)
        institution = InstitutionProfile.objects.get(initials=institution_initials)
        self.queryset = institution.services.all()
        return self.queryset

class ServiceDeleteByInstitution(generics.DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ContainerCreate(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerDetail(generics.RetrieveDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

