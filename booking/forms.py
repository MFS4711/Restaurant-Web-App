# Standard library imports
from datetime import datetime, timedelta

# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.safestring import mark_safe

# Local application imports
from .models import Table, Booking
from .utils import (
    generate_time_slots,
    is_table_available,
    generate_conflicting_time_range,
    OPENING_HOURS
)


class FifteenMinuteIntervalTimeWidget(forms.TimeInput):
    """
    Custom time input widget that allows selecting time in 15-minute intervals.
    It renders an HTML time input field along with a
    datalist of available time slots.
    """

    def __init__(self, *args, **kwargs):
        # Ensure that any custom attributes are handled properly
        kwargs['attrs'] = kwargs.get('attrs', {})
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        """
        Renders the time input widget along with a datalist
        that contains available times.

        The available times are generated using the
        `generate_available_times` method,
        and then inserted into the HTML for time selection.
        """
        available_times = self.generate_available_times()
        html = super().render(name, value, attrs, renderer)
        datalist = f'<datalist id="{name}_times">'

        # Add available time slots to the datalist
        for time in available_times:
            datalist += f'<option value="{time}">{time}</option>'
        datalist += '</datalist>'

        # Modify input HTML to link the datalist
        input_html = html.replace('>', f' list="{name}_times">')
        return mark_safe(input_html + datalist)

    def generate_available_times(self):
        """
        Generates available time slots based on 15-minute intervals.

        This method calls `generate_time_slots` from utils.py
        to fetch the available slots.
        """
        return generate_time_slots()


class BookingForm(forms.ModelForm):
    """
    Form for creating and updating bookings.

    Allows users to select the booking date, time, number of people,
    and any additional notes.
    Includes custom widgets and validation for time intervals
    and date restrictions.
    """

    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_people', 'additional_notes']

    # Custom date field widget with restrictions
    date = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Date format for HTML5 date input
            attrs={
                'type': 'date',
                'class': 'form-control',
                # Restrict booking to dates - 2 days in future for non-staff
                'min': (
                        (timezone.now().date() + timedelta(days=2))
                        .strftime('%Y-%m-%d')
                ),
            }
        )
    )

    # Custom time field widget for 15-minute intervals
    time = forms.TimeField(
        widget=FifteenMinuteIntervalTimeWidget(
            format='%H:%M',  # Time format for HTML5 time input
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': 900,  # 15-minute intervals (900 seconds)
            }
        )
    )

    # Number of people field with a restricted range (1 to 12)
    number_of_people = forms.IntegerField(
        min_value=1,  # Minimum number of people is 1
        max_value=12,  # Maximum number of people is 12
        widget=forms.NumberInput(
            attrs={
                'type': 'number',  # Use HTML5 number input type
                'class': 'form-control',
                'min': 1,
                'max': 12,  # Limit to a maximum of 12 people
                'step': 1,  # Increment by 1
            }
        )
    )

    def clean_date(self):
        """
        Custom validation for the date field.

        Ensures non-staff users cannot book a table for less
        than 2 days from today.
        """
        date = self.cleaned_data.get("date")

        # Check if the user is non-staff
        if self.instance.user and not self.instance.user.is_staff:
            now = timezone.now().date()  # Get current date
            if date < now + timedelta(days=2):
                raise ValidationError(
                    "You cannot book a table for less than 2 days from today."
                )
        return date

    def clean_time(self):
        """
        Custom validation for the time field.

        Ensures the selected time is within the restaurant's opening hours.
        """
        time = self.cleaned_data.get("time")

        # Get the opening and closing times for today
        open_time, close_time = (
            OPENING_HOURS.get(datetime.now().weekday(),
                              {"open": "16:00", "close": "22:00"})
            .values()
        )

        # Convert to datetime objects for comparison
        open_time = datetime.strptime(open_time, "%H:%M").time()
        close_time = datetime.strptime(close_time, "%H:%M").time()

        if time < open_time or time > close_time:
            raise ValidationError(
                f"The selected time must be between "
                f"{open_time.strftime('%H:%M')} and "
                f"{close_time.strftime('%H:%M')}."
            )

        return time


class StaffBookingForm(forms.ModelForm):
    """
    Form for staff to create or update bookings,
    including table selection and booking status.

    Fields:
    - `time`: The time of the booking.
    - `table`: The table being booked.
    - `status`: The booking status (e.g., confirmed, cancelled).
    """

    class Meta:
        model = Booking
        fields = ['time', 'table', 'status']

    time = forms.TimeField(
        widget=FifteenMinuteIntervalTimeWidget(
            format='%H:%M',  # 15-minute intervals
            attrs={'type': 'time', 'class': 'form-control', 'step': 900}
        )
    )

    # Exclude 'Pending' and 'No Show' from status choices
    status = forms.ChoiceField(
        choices=[(status, label) for status, label in Booking.STATUS_CHOICES
                 if status not in [Booking.PENDING, Booking.NO_SHOW]],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and filters available tables based
        on the booking date, time, and the number of people.
        """
        super().__init__(*args, **kwargs)

        # Get the number of people (either from the instance or initial data)
        number_of_people = (
            self.instance.number_of_people
            if self.instance and self.instance.id
            else kwargs.get('initial', {}).get('number_of_people', 1)
        )

        # Get the booking date and time (from the instance or initial data)
        booking_date = (
            self.instance.date
            if self.instance and self.instance.id
            else kwargs.get('initial', {}).get('date')
        )

        booking_time = (
            self.instance.time
            if self.instance and self.instance.id
            else kwargs.get('initial', {}).get('time', None)
        )

        # If booking date and time are available, filter tables accordingly
        if booking_date and booking_time:
            (
                new_start_time, new_end_time, conflicting_time_range_start,
                conflicting_time_range_end
            ) = generate_conflicting_time_range(
                booking_date, booking_time
            )

            self.fields['table'].queryset = Table.objects.filter(
                is_available=True,
                capacity__gte=number_of_people
            )

    def clean_table(self):
        """
        Validates the selected table to ensure it's
        available for the chosen booking time.

        Ensures no conflicts with existing bookings within
        2 hours of the selected time.
        """
        table = self.cleaned_data['table']
        booking_time = self.cleaned_data['time']
        booking_date = (
            self.instance.date
            if self.instance and self.instance.id
            else self.cleaned_data['date']
        )

        # Generate conflicting time range based on booking date and time
        new_start_time, new_end_time, _, _ = generate_conflicting_time_range(
            booking_date, booking_time
        )

        if not is_table_available(
            table, booking_date, new_start_time, new_end_time
        ):
            raise ValidationError(
                f"This table is already booked within 2 hours of the \
                selected time. Please choose another time."
            )
        return table


class CustomerConfirmationForm(forms.ModelForm):
    """
    A form used by customers to confirm or cancel their booking status.

    Fields:
    - `status`: The booking confirmation status,
    limited to 'Confirmed' or 'Cancelled'.
    """

    class Meta:
        model = Booking
        fields = ['status']

    status = forms.ChoiceField(
        # Only 'Confirmed' and 'Cancelled' are available choices
        choices=Booking.STATUS_CHOICES[1:3],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BookingFilterForm(forms.Form):
    """
    A form for filtering bookings based on different date ranges.

    Fields:
    - `filter`: A choice field for selecting the filter type (this week,
    this month, or custom).
    - `start_date`: The start date for custom filtering.
    - `end_date`: The end date for custom filtering.
    """

    FILTER_CHOICES = [
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('custom', 'Custom'),
    ]

    filter = forms.ChoiceField(choices=FILTER_CHOICES, required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))

    def clean(self):
        """
        Custom validation to ensure that both `start_date` and
        `end_date` are provided when 'custom' filter is selected.
        """
        cleaned_data = super().clean()
        filter_duration = cleaned_data.get('filter')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if filter_duration == 'custom' and (not start_date or not end_date):
            raise forms.ValidationError(
                "Both start and end dates must be provided for custom range.")
        return cleaned_data

    def get_filtered_date_range(self):
        """
        Returns the date range based on the selected filter type.
        - 'this_week' calculates the current week's range.
        - 'this_month' calculates the current month's range.
        - 'custom' uses user-provided start and end dates.
        """
        today = timezone.now().date()
        filter_duration = self.cleaned_data.get('filter')

        if filter_duration == 'this_week':
            # Start of the current week (Monday)
            start_date = today - timedelta(days=today.weekday())
            # End of the current week (Sunday)
            end_date = start_date + timedelta(days=6)
        elif filter_duration == 'this_month':
            start_date = today.replace(day=1)  # Start of the current month
            # End of the current month (last day)
            end_date = (start_date.replace(
                month=start_date.month + 1) - timedelta(days=1))
        elif filter_duration == 'custom':
            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
        else:
            # Default to today if no filter is selected
            start_date = end_date = today

        return start_date, end_date
