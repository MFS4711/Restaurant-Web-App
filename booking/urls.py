from django.urls import path
from . import views

urlpatterns = [
    # View to handle table booking
    path('book-table/', views.book_table, name='book_table'),

    # View to display the booking success page
    path('booking-success/', views.booking_success, name='booking_success'),

    # View to delete a specific booking
    path('delete-booking/<int:booking_id>/',
         views.delete_booking, name='delete_booking'),

    # View to edit a specific booking
    path('edit-booking/<int:booking_id>/',
         views.edit_booking, name='edit_booking'),

    # View to manage existing bookings
    path('manage-booking/', views.manage_bookings, name='manage_bookings'),
]
