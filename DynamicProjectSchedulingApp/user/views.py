from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.serializers import UserSerializer, AuthTokenSerializer

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """
    View for creating user
    """

    serializer_class = UserSerializer

