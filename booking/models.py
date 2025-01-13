from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Table model


class Table(models.Model):
    """
    Represents a table in the restaurant.

    This model stores information about a table in the restaurant,
    such as its table number, seating capacity, and availability status.

    Attributes:
        table_number (str): A unique identifier for the table
        (e.g., "A1", "B3").
        capacity (int): The maximum number of people
        that can be seated at the table.
        is_available (bool): A boolean indicating whether the table
        is available for booking.

    Methods:
        __str__(): Returns a string representation of the table,
        including its table number and capacity.
    """
    table_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} --- {self.capacity} seats"


# Booking model
class Booking(models.Model):
    """
    Represents a booking made by a user for a table in the restaurant.

    This model stores details of a booking, including the user who made the
    booking, the date and time of the booking, the number of people,
    and the assigned table.

    Attributes:
        user (User): A foreign key relationship to the User model, representing
        the user making the booking.
        date (DateField): The date of the booking.
        time (TimeField): The time of the booking.
        number_of_people (int): The number of people included in the booking.
        additional_notes (str): Any additional notes provided by the user
        regarding the booking.
        status (str): The current status of the booking
        (e.g., "pending", "confirmed", etc.).
        table (Table): A foreign key relationship to the Table model,
        representing the table reserved for the booking.
        created_at (DateTimeField): The date and time when the
        booking was created.
        updated_at (DateTimeField): The date and time when the booking
        was last updated.
        approved_by (User): A foreign key relationship to the User model,
        representing the user who approved the booking (optional).

    Methods:
        __str__(): Returns a string representation of the booking,
        including its ID, user, date, and time.
        get_end_time(): Returns the calculated end time of the booking,
        assuming a 2-hour duration.
        save(): Custom save method to handle table clearing when the
        booking is cancelled.
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
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=PENDING)
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='bookings',
        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_bookings')

    def __str__(self):
        """
        Returns a string representation of the booking.

        This includes the booking ID, the username of the user who made
        the booking, the date, and the time of the booking.
        """
        return (f"Booking {self.id} by {self.user.username} "
                f"on {self.date} at {self.time}")

    def get_end_time(self):
        """
        Returns the end time of the booking.

        This assumes a fixed 2-hour duration for all bookings
        (you can modify this logic if needed).
        The function calculates the end time by adding
        2 hours to the start time.

        Returns:
            datetime: The end time of the booking, considering the
            start time and a 2-hour duration.
        """
        # Get the start time of the booking
        start_time = timezone.make_aware(
            datetime.combine(self.date, self.time))
        # Assuming all bookings last 2 hours
        end_time = start_time + timedelta(hours=2)
        return end_time

    def save(self, *args, **kwargs):
        """
        Custom save method to handle table clearing when the
        booking status is set to 'Cancelled'.

        If the booking status is changed to 'Cancelled',
        the table assignment is cleared before saving the booking.
        """
        # Check if the table is available before saving the booking
        if self.table and not self.table.is_available:
            raise ValueError(
                "The selected table is not available for booking."
            )

        # If the booking status is set to 'Cancelled', clear the assigned table
        if self.status == Booking.CANCELLED:
            self.table = None

        # Now proceed with saving the booking
        super().save(*args, **kwargs)

    class Meta:
        """
        Specifies that no two bookings can occupy the
        same table at the same time.

        This ensures that the combination of date, time, and table is unique,
        preventing double bookings.
        """
        unique_together = ('date', 'time', 'table')
