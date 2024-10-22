from django.shortcuts import render

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

class solicitud(TemplateView):
    template_name = 'index.html'
