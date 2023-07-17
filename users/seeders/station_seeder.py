from faker import Faker
from ..models import Station
import random
from django.contrib.gis.geos import Point
class StationSeeder:

    def generate_sample_stations(self,num_samples=50):
        fake = Faker()
        stations = []
        for _ in range(num_samples):
            name = fake.city()
            latitude = random.uniform(-4.672441, 4.622503)
            longitude = random.uniform(33.893381, 41.899262)
            stations.append({'name': name, 'latitude': latitude, 'longitude': longitude})
        return stations
    
    def create_stations(self,station_data):

        stations = [Station(name=data['name'], location=Point((data['longitude'],data['latitude']))) for data in station_data]
        Station.objects.bulk_create(stations)
        return stations
    

    def run(self):
        data = self.generate_sample_stations(200)
        self.create_stations(data)


