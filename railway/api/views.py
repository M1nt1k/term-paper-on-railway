from rest_framework import generics, permissions, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated

from .serializers import *
from .models import *
from user.models import User
from rails.models import *
# from .permissions import IsOwnerOrReadOnly

class ProfileViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_class = (IsAuthenticated,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

class TrainViewset(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_class = (AllowAny,)

class CarriageViewset(viewsets.ModelViewSet):
    queryset = Carriage.objects.all()
    serializer_class = CarriageSerializer
    permission_class = (AllowAny,)

class TicketViewset(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_class = (AllowAny,)

class PlacesViewset(viewsets.ModelViewSet):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    permission_class = (AllowAny,)




