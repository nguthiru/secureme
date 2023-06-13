from django.urls import include,path,re_path
from .views import *
urlpatterns = [
    path('login/',login_view,name='login'),
    path('approval-request/',approval_request_view,name='approval-request'),
    path('', include('dj_rest_auth.urls')),
    path('register/', include('dj_rest_auth.registration.urls'))

]