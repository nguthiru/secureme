from rest_framework import serializers

from users.models import Station
from datetime import date, datetime
from .models import Crime
import json
class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'

class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = '__all__'