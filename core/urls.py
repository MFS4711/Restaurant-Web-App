from django.urls import path
from . import views

urlpatterns = [
    # View to render the contact page
    path('contact/', views.contact, name='contact'),

    # View to render the homepage
    path('', views.homepage, name='home'),
]