from enum import Enum
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from users.models import User
from users.api.serializers import UserSerializer


class ErrorMessages(Enum):
    NO_TOKEN = 'No Token. Authorization Denied'
    NO_CREDENTIALS = 'Please provide both email and password'
    INVALID_CREDENTIALS = 'Invalid Credentials'


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            token = Token.objects.get(user_id=serializer.data.get('id'))
            return Response(data={'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthUserView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request) -> Response:
        token: str = request.headers.get('Authorization')
        if not token:
            return Response(data={'error': ErrorMessages.NO_TOKEN.value}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(id=request.user.id)
        data = UserSerializer(user).data
        return Response(data)

    def post(self, request: Request) -> Response:
        email: str = request.data.get('email')
        password: str = request.data.get('password')

        if email == '' or password == '':
            return Response({'error': ErrorMessages.NO_CREDENTIALS.value},
                            status=status.HTTP_400_BAD_REQUEST)

        user: User = authenticate(username=email, password=password)

        if not user:
            return Response({'error': ErrorMessages.INVALID_CREDENTIALS.value},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token', token.key}, status=status.HTTP_200_OK)
