from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Table, Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_people', 'additional_notes',]

    # Custom widget for the date field
    date = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Format to match the HTML5 date input format
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().strftime('%Y-%m-%d'),  # Disable past dates
            }
        )
    )

    # Custom widget for the time field
    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',  # Format to match the HTML5 time input format
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': 900,
            }
        )
    )

    # Custom widget for the number of people field
    number_of_people = forms.IntegerField(
        min_value=1,  # Minimum value of 0
        max_value=12,  # Maximum value of 12
        widget=forms.NumberInput(
            attrs={
                'type': 'number',  # HTML5 number input type
                'class': 'form-control',
                'min': 1,
                'max': 12,  # Max to match max table
                'step': 1,  # Increment by 1
            }
        )
    )


class StaffBookingForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Booking
        # Only allow status and table for staff
        fields = ['time', 'table', 'status']

    # Custom widget for the time field
    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',  # Format to match the HTML5 time input format
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': 900,
            }
        )
    )

    # Custom widget for the table selection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the instance exists and number_of_people is available
        if self.instance and self.instance.id:
            number_of_people = self.instance.number_of_people
        else:
            # Default to 0 if it's a new booking
            number_of_people = kwargs.get(
                'initial', {}).get('number_of_people', 1)

        # Filter tables that:
        # - Are available (is_available=True)
        # - Have sufficient capacity for the number of people
        # - Are not already booked at the same date/time (if it's not a new booking)
        self.fields['table'].queryset = Table.objects.filter(
            is_available=True,
            # Ensure table capacity is greater or equal to the number of people
            capacity__gte=number_of_people
        ).exclude(
            bookings__date=self.instance.date,
            bookings__time=self.instance.time
        ) if self.instance and self.instance.id else Table.objects.filter(
            is_available=True,
            capacity__gte=number_of_people
        )

    def clean_table(self):
        # Access cleaned data (table and time)
        table = self.cleaned_data['table']
        booking_time = self.cleaned_data['time']

        # Get the date for this booking
        booking_date = self.instance.date if self.instance and self.instance.id else self.cleaned_data[
            'date']

        # Calculate the new booking's start and end times
        new_start_time = timezone.make_aware(
            datetime.combine(booking_date, booking_time))
        new_end_time = new_start_time + timedelta(hours=2)

        # 2-hour delta for comparison
        delta = timedelta(hours=2)

        # Fetch all bookings for the selected table on the selected date
        conflicting_bookings = Booking.objects.filter(
            table=table,
            date=booking_date
            # Exclude the current booking if updating
        ).exclude(id=self.instance.id if self.instance else None)

        # Check for time conflicts
        for booking in conflicting_bookings:
            existing_start_time = timezone.make_aware(
                datetime.combine(booking.date, booking.time))
            existing_end_time = existing_start_time + timedelta(hours=2)

            # If the new booking overlaps within the 2-hour window, raise an error
            if (new_start_time < existing_end_time and new_end_time > existing_start_time):
                raise ValidationError(
                    f"This table is already booked within 2 hours of the selected time. Please choose another time.")

        return table
