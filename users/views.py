from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from users.models import ApprovalRequests, CustomUser, Station

from users.serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        if user.approved:
            login(request, user)
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful.','token':token.key,'user':UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Your account is not approved.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST']) 
def approval_request_view(request):
    user_email = request.data.get('email')
    station = request.data.get('station')

    if user_email is None or station is None:
        return Response({'error': 'Please provide email and station.'}, status=status.HTTP_400_BAD_REQUEST)
    user = CustomUser.objects.get(email=user_email)
    station = Station.objects.get(id=station)

    if user is not None:
        if user.approved:
            return Response({'error': 'User is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            approval_request = ApprovalRequests.objects.create(user=user,station=station)
            return Response({'message': 'The user has been approved'}, status=status.HTTP_200_OK)

    