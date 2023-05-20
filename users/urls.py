from django.urls import include,path,re_path
urlpatterns = [
    re_path(r'^rest-auth/', include('rest_auth.urls'))
]