from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.
# Table model


class Table(models.Model):
    """

    """
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} --- {self.capacity} seats"


# Booking model
class Booking(models.Model):
    """

    """
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    NO_SHOW = 'no_show'
    CUSTOMER_CONFIRMATION_REQUIRED = 'customer_confirmation_required'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
        (NO_SHOW, 'No Show'),
        (CUSTOMER_CONFIRMATION_REQUIRED, 'Customer Confirmation Required'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=PENDING)
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_bookings')

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on {self.date} at {self.time}"

    def get_end_time(self):
        # Get the start time of the booking
        start_time = timezone.make_aware(
            datetime.combine(self.date, self.time))
        # Assuming all bookings last 2 hours (you can replace this with dynamic duration if needed)
        end_time = start_time + timedelta(hours=2)
        return end_time
    
    def save(self, *args, **kwargs):
        # If the booking status is being set to 'Cancelled', clear the assigned table
        if self.status == Booking.CANCELLED:
            self.table = None

        # Now proceed with saving the booking
        super().save(*args, **kwargs)

    # Ensure no two bookings can occupy the same table at the same time
    class Meta:
        unique_together = ('date', 'time', 'table')
