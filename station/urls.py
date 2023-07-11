from django.urls import include,path,re_path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('crime', CrimeViewSet, basename='crime')
urlpatterns = [
    path('stations/',get_all_stations),
    path('check_criminal/<int:id_number>/',check_if_criminal_exists),
    path('criminal/add/',add_criminal),
    path('criminal/search/',search_criminal),
    path('criminal/crime/connect/',connect_crime),
    path('criminal/accomplice/connect/',connect_accomplice)

]
urlpatterns += router.urls
