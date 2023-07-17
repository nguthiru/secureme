from django.urls import include,path,re_path
from .views import *
urlpatterns = [
    path('login/',login_view,name='login'),
    path('approval-request/',approval_request_view,name='approval-request'),
    # path('', include('dj_rest_auth.urls')),
    path('register/', register, name='register'),
    path('activate/email/', validate_email_activate_account, name='activate'),
    path('activate/email/resend/', resend_validation_email, name='resend'),
    path('password/reset/email/',reset_password_email,name='reset-password-email'),
    path('password/reset/verify/',validate_reset_code,name='verify-reset-code'),
    path('password/reset/<str:grant_token>/',reset_password,name='reset-password'),
    path('user/',get_user,name='get-user'),
    path('station/seed/',run_station_seeder,name='seed-stations'),
]