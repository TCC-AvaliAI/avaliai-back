from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from social_django.utils import load_strategy
from suap_backend.backends import SuapOAuth2


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
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)