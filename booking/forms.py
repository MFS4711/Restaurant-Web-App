from django import forms
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
        fields = ['table', 'status']  # Only allow status and table for staff
    
    # Custom widget for the table selection
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the instance exists and number_of_people is available
        if self.instance and self.instance.id:
            number_of_people = self.instance.number_of_people
        else:
            # Default to 0 if it's a new booking
            number_of_people = kwargs.get('initial', {}).get('number_of_people', 1)
        
        # Filter tables that:
        # - Are available (is_available=True)
        # - Have sufficient capacity for the number of people
        # - Are not already booked at the same date/time (if it's not a new booking)
        self.fields['table'].queryset = Table.objects.filter(
            is_available=True,
            capacity__gte=number_of_people  # Ensure table capacity is greater or equal to the number of people
        ).exclude(
            bookings__date=self.instance.date,
            bookings__time=self.instance.time
        ) if self.instance and self.instance.id else Table.objects.filter(
            is_available=True,
            capacity__gte=number_of_people
        )

    table = forms.ModelChoiceField(
        queryset=Table.objects.all(),  # Default queryset, will be filtered on initialization
        widget=forms.Select(attrs={'class': 'form-control'})
    )