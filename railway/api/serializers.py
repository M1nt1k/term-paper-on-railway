from rest_framework import serializers
from .models import *
from user.models import User
from rails.models import *

class TrainSerializer(serializers.ModelSerializer):
    carriages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    train_addons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Train
        fields = ['id', 'name', 'start_time', 'end_time', 'start_city', 'end_city', 'carriages', 'train_addons']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['start_city'] = instance.start_city.name
        response['end_city'] = instance.end_city.name

        return response

class TicketSerializer(serializers.ModelSerializer):
    # profile = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # train = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # carriage = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # place = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields  = ['id', 'user', 'train', 'carriage', 'places']

class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    # city = serializers.ReadOnlyField(source='city.name')
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'third_name', 'birthday', 'tickets']

class CitySerializer(serializers.ModelSerializer):
    train = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'train']

class CarriageSerializer(serializers.ModelSerializer):
    places = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # train = serializers.ReadOnlyField(source='train.name')

    class Meta:
        model = Carriage
        fields = ['id', 'train', 'number', 'place_type', 'places']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['train'] = instance.train.name

        return response

class PlacesSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # carriage = serializers.ReadOnlyField(source='carriage.name')

    class Meta:
        model = Places
        fields = ['id', 'carriage', 'user', 'number', 'status']
