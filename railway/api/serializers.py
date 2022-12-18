from rest_framework import serializers
from .models import *

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
        fields = fields = ['id', 'profile', 'train', 'carriage', 'places']

class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    # city = serializers.ReadOnlyField(source='city.name')
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'third_name', 'birthday', 'pass_serial', 'pass_number', 'tickets']

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
        fields = ['id', 'carriage', 'profile', 'number', 'status']

class AddonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addons
        fields = ['id', 'addon', 'train']

class UserRegistrSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user