from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import make_aware
from .models import Table, Booking
from django.utils.safestring import mark_safe

# Custom Time Input Widget
class FifteenMinuteIntervalTimeWidget(forms.TimeInput):
    """

    """
    def __init__(self, *args, **kwargs):
        self.selected_date = kwargs.pop('selected_date', None)  # Capture the selected date
        kwargs['attrs'] = kwargs.get('attrs', {})
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Generate the list of available times (15-minute intervals) based on the selected date
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
        if not self.selected_date:
            return []  # If no date is provided, return empty list

        # Get the day of the week for the selected date (0 = Monday, 6 = Sunday)
        selected_day = self.selected_date.weekday()

        # Define the start and end times based on the selected day of the week
        if selected_day in [0, 1, 2, 3]:  # Monday to Thursday
            start_time_str = "17:00"  # Start at 5:00 PM
            end_time_str = "20:30"    # End at 8:30 PM
        elif selected_day in [4, 5]:  # Friday and Saturday
            start_time_str = "16:00"  # Start at 4:00 PM
            end_time_str = "22:00"    # End at 10:00 PM
        else:  # Sunday
            start_time_str = "16:00"  # Start at 4:00 PM
            end_time_str = "21:00"    # End at 9:00 PM

        # Convert start and end times to datetime objects
        start_time = datetime.strptime(start_time_str, "%H:%M")
        end_time = datetime.strptime(end_time_str, "%H:%M")
        
        # Generate times in 15-minute intervals
        times = []
        while start_time <= end_time:
            times.append(start_time.strftime("%H:%M"))
            start_time += timedelta(minutes=15)
        
        return times


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pass the selected date to the time widget if it's present
        selected_date = self.initial.get('date') or self.instance.date
        if selected_date:
            self.fields['time'].widget.selected_date = selected_date


class StaffBookingForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Booking
        # Only allow status and table for staff
        fields = ['time', 'table', 'status']

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

    # Custom widget for the table selection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pass the selected date to the time widget if it's present
        selected_date = self.initial.get('date') or self.instance.date
        if selected_date:
            self.fields['time'].widget.selected_date = selected_date

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
            new_start_time = make_aware(
                datetime.combine(booking_date, booking_time))
            new_end_time = new_start_time + timedelta(hours=2)

            # Extend the window to 2 hours before and after the selected time
            conflicting_time_range_start = new_start_time - timedelta(hours=2)
            conflicting_time_range_end = new_end_time + timedelta(hours=2)

            # Filter tables that:
            # - Are available (is_available=True)
            # - Have sufficient capacity for the number of people
            # - Are not already booked at the same date/time (if it's not a new booking)
            self.fields['table'].queryset = Table.objects.filter(
                is_available=True,
                capacity__gte=number_of_people
            ).exclude(
                bookings__date=booking_date,
                # Exclude bookings starting after the window
                bookings__time__gte=conflicting_time_range_start.time(),
                # Exclude bookings ending before the window
                bookings__time__lt=conflicting_time_range_end.time()
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
