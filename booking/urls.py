from django.urls import path
from . import views

urlpatterns = [
    path('book-table/', views.book_table, name='book_table'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('manage-booking/', views.manage_bookings, name='manage_bookings'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
