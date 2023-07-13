from django.urls import path
from .views import *


urlpatterns = [
    path('crime/arrests/',get_all_crime_arrests),
    path('crime/polygon/',crimes_within_polygon),
    path('criminal/arrests/location/<int:criminal_id>/',get_criminal_arrest_locations),
    path('criminal/arrests/<int:criminal_id>/',get_criminal_arrests_details),
]