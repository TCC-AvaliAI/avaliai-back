from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("logout/", LogoutView, name="logout"),
    path("login/suap/", SuapLoginView.as_view(), name="suap-login"),
]