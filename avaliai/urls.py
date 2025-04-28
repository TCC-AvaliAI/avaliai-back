"""
URL configuration for avaliai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="AvaliAI API",
        default_version="v1",
        description="Documentação da API do AvaliAI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@avaliai.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', include('django.contrib.auth.urls')),
    path('', include('social_django.urls'), name='social'),
    path('api/user/', include('apps.user.urls')),
    path('api/disciplines/', include('apps.discipline.urls')),
    path('api/classrooms/', include('apps.classroom.urls')),
    path('api/questions/', include('apps.question.urls')),
    path('api/exams/', include('apps.exam.urls')),
    path('api/messages/', include('apps.message.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

admin.site.site_header = 'AvaliAI'
admin.site.site_title = 'AvaliAI'
admin.site.index_title = 'AvaliAI'