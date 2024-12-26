from . import views
from django.urls import path

urlpatterns = [
    path('booking/', views.booking, name='booking'),
]
