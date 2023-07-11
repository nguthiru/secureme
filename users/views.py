import datetime
import hashlib
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from users.emails import send_reset_email, send_validation_email
from users.models import (
    ApprovalRequests,
    CustomUser,
    PasswordReset,
    Station,
    ValidationEmailCodes,
)
from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# Create your views here.
USER_MODEL = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")
    email = request.data.get("email")
    username = request.data.get("username")

    if password1 == None or password2 == None or email == None:
        return Response({"error": "Fill in all required fields"}, status=400)

    if password1 != password2:
        return Response({"error": "Passwords do not match"}, status=400)
    else:
        try:
            user = USER_MODEL.objects.get(email=email)
            return Response({"error": "User already exists"}, status=400)
        except USER_MODEL.DoesNotExist:
            user = USER_MODEL.objects.create(email=email)
            user.set_password(password1)
            user.save()
            send_validation_email(user)
            return Response(
                {
                    "message": "User Registration successful. An email has been sent to activate your account"
                },
                status=201,
            )


@api_view(["POST"])
def validate_email_activate_account(request):
    if "code" in request.data and "email" in request.data:
        user = get_object_or_404(USER_MODEL, email=request.data.get("email"))
        if user.activated:
            return Response(
                {"error:": "Account is already active"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        time_threshold = datetime.now() - timedelta(minutes=14)
        code = request.data.get("code")
        validation_codes = ValidationEmailCodes.objects.filter(
            user=user, date_requested__gt=time_threshold, code_used=False
        )
        validation_code = validation_codes.latest("date_requested")
        if str(code) == str(validation_code.code):
            user.activated = True
            validation_code.code_used = True
            validation_code.save()
            user.save()
            return Response({"message": "Account Activated successfully"}, status=200)
        else:
            return Response({"error": f"Incorrect Code entered "}, status=400)
    else:
        return Response({"error": "Fill in all required fields"}, status=400)


@api_view(["POST"])
def resend_validation_email(request):
    if "email" in request.data:
        user = get_object_or_404(USER_MODEL, email=request.data.get("email"))
        if user.activated:
            return Response(
                {"error": "Account is already active"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if send_validation_email(user):
            return Response(
                {"message": "Email sent successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "An error has occured"}, status=status.HTTP_502_BAD_GATEWAY
            )

    else:
        return Response(
            {"error": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)

    if user is not None:
        if not user.activated:
            return Response(
                {"error": "Your email address is not verified."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "message": "Login successful.",
                "token": token.key,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

    else:
        return Response(
            {"error": "Invalid login credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
def approval_request_view(request):
    station = request.data.get("station")
    police_id = request.data.get("police_id")
    work_id = request.data.get("work_id")
    user_type = request.data.get("user_type")
    print(user_type)
    if user_type is None:
        return Response(
            {"error": "Please provide your user type."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if user_type == 'P' and (police_id is None or station is None):
        return Response(
            {"error": "Please provide your police and station."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user_type == 'A' and work_id is None:
        return Response(
            {"error": "Please provide your work id."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = request.user


    
    if user.approved:
        return Response(
            {"error": "User is already approved."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
        
    else:
        previous_requests = ApprovalRequests.objects.filter(user=user).first()
        if previous_requests is not None:
            return Response(
                {"error": "You have already sent an approval request."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user_type == 'P':
            station = Station.objects.get(id=station)

            approval_request = ApprovalRequests.objects.create(user=user, station=station,user_type='police')

        elif user_type == 'A':
            approval_request = ApprovalRequests.objects.create(user=user, user_type='analytics',work_id=work_id)

        return Response(
            {
                "message": "Your approval request has been sent.",
                "approval": {"id": approval_request.id},
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_email(request):
    if "email" in request.data:
        email = request.data.get("email")
        try:
            user = USER_MODEL.objects.get(email=email)
            if send_reset_email(user):
                return Response(
                    {"message": "Email sent successfully", "email": user.email},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "An error has occured"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "error": "There is no user asscoaited with that email please register"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    else:
        return Response(
            {"error": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def validate_reset_code(request):
    if "code" in request.data:
        user = get_object_or_404(USER_MODEL, email=request.data.get("email"))
        time_threshold = datetime.now() - timedelta(minutes=14)
        code = request.data.get("code")
        password_resets = PasswordReset.objects.filter(
            user=user, date_requested__gt=time_threshold, code_used=False
        )
        password_reset = password_resets.latest("date_requested")
        if str(code) == str(password_reset.reset_code):
            to_encode: str = (
                request.data.get("email")
                + str(code)
                + str(int(datetime.now().timestamp()))
            )
            grant_token = hashlib.md5(to_encode.encode()).hexdigest()
            password_reset.grant_token = grant_token
            password_reset.is_valid = True
            password_reset.save()
            return Response(
                {"grant_token": grant_token, "email": user.email}, status=200
            )
        else:
            return Response({"error": f"Incorrect Code"}, status=400)
    else:
        return Response(status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, grant_token):
    if "password1" in request.data and "password2" in request.data:
        time_threshold = datetime.now() - timedelta(minutes=14)

        pass_request = get_object_or_404(
            PasswordReset,
            grant_token=grant_token,
            is_valid=True,
            date_requested__gt=time_threshold,
            code_used=False,
        )
        user = pass_request.user
        pass1 = request.data.get("password1")
        pass2 = request.data.get("password2")
        if pass1 == pass2:
            user.set_password(pass1)
            pass_request.code_used = True
            pass_request.save()
            user.save()
            return Response({"message": "Password reset successful"}, status=200)
        else:
            return Response({"error": "Passwords do not match"}, status=400)
    else:
        return Response({"error": "Some fields are missing"}, status=400)


@api_view(['GET'])
def get_user(request):

    user = request.user
    if user.is_authenticated:
        return Response(UserSerializer(user).data, status=200)

    else:
        return Response(
            {"error": "Invalid Token."}, status=status.HTTP_401_UNAUTHORIZED
        )
    
