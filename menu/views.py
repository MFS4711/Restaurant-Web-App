from django.shortcuts import render
from django.views.generic import TemplateView

def homepage(request):

    return render(request, "menu/index.html")
