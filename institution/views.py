from rest_framework import generics
from institution.models import InstitutionProfile, Service, Container
from institution.serializers import InstitutionProfileSerializer, ServiceSerializer, ContainerSerializer

class InstitutionDetail(generics.RetrieveAPIView):
    queryset = InstitutionProfile.objects.all()
    serializer_class = InstitutionProfileSerializer

    lookup_field = "initials"
    lookup_url_kwarg = "initials"

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

