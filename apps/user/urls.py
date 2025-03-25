from django.urls import path
from .views import IndexView, LogoutView, SuapLoginView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/suap/", SuapLoginView.as_view(), name="suap-login"),
]