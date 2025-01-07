from django.urls import path
from . import views

urlpatterns = [
    path('customer-dashboard/<int:user_id>', views.customer_dashboard, name='customer_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]