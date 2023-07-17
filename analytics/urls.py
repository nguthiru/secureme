from django.urls import path
from .views import *


urlpatterns = [
    path('crime/arrests/',get_all_crime_arrests),
    path('crime/arrests/filter/',get_crime_arrests_filtered_by_crime),
    path('crime/polygon/',crimes_within_polygon),
    path('criminal/arrests/location/<int:criminal_id>/',get_criminal_arrest_locations),
    path('criminal/arrests/<int:criminal_id>/',get_criminal_arrests_details),
    path('criminal/accomplice/<int:criminal_id>/',criminal_accomplice_network),
    path('crime/station/trend/<int:station>/total/',crime_station_total_trend, name='crime_station_chart'),
]