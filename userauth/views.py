from http.client import responses

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .models import CustomUSer
from .serializers import SignUpSerializer,ProfileSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            'status': status.HTTP_201_CREATED,
            'message': user.username
        }
        return Response(response)


class LoginView(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError({'message': 'Username yoki parol notogri'})

        token, _ = Token.objects.get_or_create(user=user)

        response = {
            'status': status.HTTP_201_CREATED,
            'message': 'Siz ruxatdan otdingiz',
            'token': str(token.key)
        }
        return Response(response)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({'message': 'Username yoki parol noto‘g‘ri'})
        if user != request.user:
            raise ValidationError({'message': 'Bu foydalanuvchi siz emassiz'})
        request.user.auth_token.delete()
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Siz tizimdan muvaffaqiyatli chiqdingiz'
        }
        return Response(response, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user=request.user
        serializer=ProfileSerializer(user)

        response={
            'status':status.HTTP_200_OK,
            'data':serializer.data
        }
        return  Response(response)