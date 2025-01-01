from django.urls import path
from . import views

urlpatterns = [
    path('customer-dashboard/<int:user_id>', views.customer_dashboard, name='customer_dashboard'),
]