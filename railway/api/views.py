from rest_framework import generics, permissions, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import *
from .models import *
# from .permissions import IsOwnerOrReadOnly

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TrainViewset(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

class CarriageViewset(viewsets.ModelViewSet):
    queryset = Carriage.objects.all()
    serializer_class = CarriageSerializer

class TicketViewset(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class PlacesViewset(viewsets.ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

class AddonsViewset(viewsets.ModelViewSet):
    queryset = Addons.objects.all()
    serializer_class = AddonsSerializer

class RegistViewset(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)

