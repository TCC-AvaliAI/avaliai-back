from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from decouple import config



class IndexView(TemplateView):
    template_name = 'index.html'


def LogoutView(request):
    logout(request)
    return redirect(config('URL_REDIRECT'))