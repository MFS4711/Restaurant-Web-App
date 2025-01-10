from django.urls import path
from . import views

urlpatterns = [
    # View to display the admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # View to display the customer dashboard for a specific user
    path('customer-dashboard/<int:user_id>', views.customer_dashboard, name='customer_dashboard'),

    # View to display the staff dashboard
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]