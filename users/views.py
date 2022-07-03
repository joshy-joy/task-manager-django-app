from re import I
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.contrib.auth.models import User

from .utils import create_response
from .permissions import set_user_permissions
from .dao import get_user

#Python package imports

#REST_Framework imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# API to register new user
class SignUp(APIView):
    def post(self, request, format=None):
        email = request.data.get('email').strip()
        password = make_password(request.data.get('password').strip())
        role = request.data.get('role').strip()

        if not (email and password and role):
            return create_response("error", "email, password and role fields are mandatory for registration", status.HTTP_400_BAD_REQUEST)
        
        if role not in ["Manager", "Employee", "Client"]:
            return create_response("error", "Invalid role", status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user(email)
            return create_response("error", "User already exist. Please login", status.HTTP_400_BAD_REQUEST)
        except:
            user = User(username=email, password=password)
            user.save()
            set_user_permissions(role, user)
            return create_response("success", "User cretaed successfully", status.HTTP_200_OK)


# API to login
class Login(APIView):
    def get(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not (email and password):
            return create_response("error",'email and password missing', status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user(email)
            if django_pbkdf2_sha256.verify(password, user.password):
                refresh = RefreshToken.for_user(user)
                token = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                return create_response("success", "login success", status.HTTP_200_OK, token)

            return create_response("error", "password mismatch", status.HTTP_400_BAD_REQUEST)
        except:
                return create_response("error", "User not found", status.HTTP_404_NOT_FOUND)


