from django.views.generic import TemplateView
from django.contrib.auth import logout, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from social_django.utils import load_strategy
from suap_backend.backends import SuapOAuth2
from rest_framework.permissions import AllowAny
from decouple import config

import requests

class IndexView(TemplateView):
    template_name = 'index.html'


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


class SuapLoginView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]  

    def post(self, request):
        access_token = request.headers.get('Authorization')
        if not access_token:
            return Response({"error": "Access token is required in the Authorization header"}, status=status.HTTP_400_BAD_REQUEST)
        if access_token.startswith("Bearer "):
            access_token = access_token[7:]
        strategy = load_strategy(request)
        backend = SuapOAuth2(strategy=strategy)
        try:
            user = backend.do_auth(access_token)
            if user:
                login(request, user)
                return Response({"message": "Login successful", "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            print(f"Erro de autenticação: {e}")  
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"Erro inesperado: {e}")  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = requests.post(
                'https://suap.ifrn.edu.br/o/token/',
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': config("SOCIAL_AUTH_SUAP_KEY"),
                    'client_secret': config("SOCIAL_AUTH_SUAP_SECRET"),
                }
            )

            if response.status_code == 200:
                tokens = response.json()
                return Response({
                    'access_token': tokens['access_token'],
                    'refresh_token': tokens.get('refresh_token', refresh_token)
                })
            else:
                return Response(
                    {"error": "Failed to refresh token"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            print(f"Erro ao fazer refresh do token: {str(e)}")
            return Response(
                {"error": "Failed to refresh token"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )