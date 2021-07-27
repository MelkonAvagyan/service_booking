from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.models import User


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class AboutPageView(generic.TemplateView):
    template_name = 'about.html'
    



