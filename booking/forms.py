from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import make_aware
from .models import Table, Booking
from django.utils.safestring import mark_safe
from .utils import generate_time_slots, is_table_available, generate_conflicting_time_range

# Custom Time Input Widget


class FifteenMinuteIntervalTimeWidget(forms.TimeInput):
    """

    """

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = kwargs.get('attrs', {})
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Generate the list of available times using the generate_time_slots function from utils.py
        available_times = self.generate_available_times()

        # Get the HTML render of the widget itself (input field)
        html = super().render(name, value, attrs, renderer)

        # Build the datalist
        datalist = f'<datalist id="{name}_times">'
        for time in available_times:
            datalist += f'<option value="{time}">{time}</option>'
        datalist += '</datalist>'

        # Insert the datalist into the widget (link it with the input field)
        input_html = html.replace('>', f' list="{name}_times">')

        # Return the input field and the datalist
        return mark_safe(input_html + datalist)

    def generate_available_times(self):
        """
        Generate available times based on the opening hours for the current day.
        Uses the generate_time_slots function from utils.py to get the slots.
        """
        # Call the utility function to generate the time slots
        return generate_time_slots()


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
                # Disable today and tomorrow
                'min': (timezone.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
            }
        )
    )

    # Custom widget for the time field
    time = forms.TimeField(
        widget=FifteenMinuteIntervalTimeWidget(
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

    # Custom validation for the date field
    def clean_date(self):
        date = self.cleaned_data.get("date")

        if self.instance.user and not self.instance.user.is_staff:  # Non-staff users
            # Get the current date and ensure the booking date is at least 2 days later
            now = timezone.now().date()  # Current date without the time
            if date < now + timedelta(days=2):
                raise ValidationError(
                    "You cannot book a table for less than 2 days from today.")

        return date


class StaffBookingForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Booking
        fields = ['time', 'table', 'status']

    # Custom widget for the time field (interval of 15 minutes)
    time = forms.TimeField(
        widget=FifteenMinuteIntervalTimeWidget(
            format='%H:%M',  # Format to match the HTML5 time input format
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': 900,  # Step is set to 900 seconds (15 minutes)
            }
        )
    )

    # Restrict the available status choices to exclude 'Pending' and 'No Show'
    status = forms.ChoiceField(
        choices=[(status, label) for status, label in Booking.STATUS_CHOICES
                 if status not in [Booking.PENDING, Booking.NO_SHOW]],  # Exclude PENDING and NO_SHOW
        widget=forms.Select(attrs={'class': 'form-control'})
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

        # Get the date for the current booking (either from instance or cleaned data)
        booking_date = self.instance.date if self.instance and self.instance.id else kwargs.get(
            'initial', {}).get('date')

        # Calculate the new start and end times for the proposed booking
        if self.instance and self.instance.id:
            booking_time = self.instance.time
        else:
            booking_time = kwargs.get('initial', {}).get('time', None)

        if booking_date and booking_time:
            # Generate start and end times for the booking
            new_start_time, new_end_time, conflicting_time_range_start, conflicting_time_range_end = generate_conflicting_time_range(
                booking_date, booking_time)

            # Filter tables that:
            # - Are available (is_available=True)
            # - Have sufficient capacity for the number of people
            # - Are not already booked at the same date/time (using the time window)
            self.fields['table'].queryset = Table.objects.filter(
                is_available=True,
                capacity__gte=number_of_people
            ).exclude(
                bookings__date=booking_date,
                bookings__time__gte=conflicting_time_range_start.time(),
                bookings__time__lt=conflicting_time_range_end.time()
            )

    def clean_table(self):
        """

        """
        # Access cleaned data (table and time)
        table = self.cleaned_data['table']
        booking_time = self.cleaned_data['time']

        # Get the date for this booking
        booking_date = self.instance.date if self.instance and self.instance.id else self.cleaned_data[
            'date']

        # Generate start and end times for the new booking
        new_start_time, new_end_time, _, _ = generate_conflicting_time_range(
            booking_date, booking_time)

        # Check if the selected table is available for the given time range
        if not is_table_available(table, booking_date, new_start_time, new_end_time):
            # If there is a conflict, raise a validation error
            raise ValidationError(
                f"This table is already booked within 2 hours of the selected time. Please choose another time.")

        return table


class CustomerConfirmationForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Booking
        # Only allow status - as all other fields confirmed
        fields = ['status']

    # Restrict the available status choices to only 'Confirmed' and 'Cancelled'
    status = forms.ChoiceField(
        # Index 1 and 2 corresponds to 'Confirmed' and 'Cancelled'
        choices=Booking.STATUS_CHOICES[1:3],
        # Optional: adds a bootstrap class for styling
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BookingFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('custom', 'Custom'),
    ]
    
    filter = forms.ChoiceField(choices=FILTER_CHOICES, required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        filter_duration = cleaned_data.get('filter')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # If custom filter is selected, both start_date and end_date must be provided
        if filter_duration == 'custom' and (not start_date or not end_date):
            raise forms.ValidationError("Both start and end dates must be provided for custom range.")

        return cleaned_data

    def get_filtered_date_range(self):
        """
        Calculate the date range based on the filter type (This Week, This Month, or Custom).
        """
        today = timezone.now().date()

        filter_duration = self.cleaned_data.get('filter')

        if filter_duration == 'this_week':
            start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
            end_date = start_date + timedelta(days=6)  # End of the week (Sunday)
        elif filter_duration == 'this_month':
            start_date = today.replace(day=1)  # Start of this month
            end_date = (start_date.replace(month=start_date.month + 1) - timedelta(days=1))  # End of the month
        elif filter_duration == 'custom':
            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
        else:
            # Default to today
            start_date = end_date = today

        return start_date, end_date