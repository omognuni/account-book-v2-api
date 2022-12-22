from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, JWTTokenSerializer


class CreateUserView(generics.CreateAPIView):
    '''user 생성'''
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    '''user login'''
    serializer_class = JWTTokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            return Response(status=status.HTTP_200_OK, data=serializer.validated_data)
