from rest_framework.serializers import ModelSerializer

from .models import CustomUser, Station

class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class UserSerializer(ModelSerializer):
    station = StationSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['email','username','user_type','station','approved']