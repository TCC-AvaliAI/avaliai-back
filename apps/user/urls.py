from django.urls import path
from .views import IndexView, LogoutView, SuapLoginView, RefreshTokenView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/suap/", SuapLoginView.as_view(), name="suap-login"),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]