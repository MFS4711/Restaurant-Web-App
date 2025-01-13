from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .forms import BookingForm
from .models import Booking, Table


class TestBookingForm(TestCase):

    def setUp(self):
        """Set up necessary data for testing booking form"""
        # Create a test user for any required authentication
        self.user = User.objects.create_user(
            username='testuser', password='password')

        # Create a test table for booking
        self.table = Table.objects.create(
            table_number="A1", capacity=4, is_available=True)

        # Get the current date
        self.current_date = timezone.now().date()

        # Valid data for booking form (3 days ahead)
        self.valid_data = {
            'date': (self.current_date + timedelta(days=3)).strftime('%Y-%m-%d'),
            'time': '12:00',
            'number_of_people': 4,
            'additional_notes': 'No special requests',
        }

        # Invalid data (date is less than 2 days away)
        self.invalid_data_date = {
            'date': (self.current_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '12:00',
            'number_of_people': 4,
            'additional_notes': 'No special requests',
        }

    def test_form_is_valid(self):
        """Test that the form is valid with correct data"""
        form = BookingForm(data=self.valid_data)
        self.assertTrue(form.is_valid(),
                        'Form should be valid with correct data')

    def test_form_is_invalid_due_to_date(self):
        """Test that the form is invalid when the date is less than 2 days away"""
        form = BookingForm(data=self.invalid_data_date)
        self.assertFalse(
            form.is_valid(), 'Form should be invalid if date is less than 2 days ahead')

    def test_date_field_min_limit(self):
        """Ensure the date field enforces the minimum limit of 2 days ahead"""
        invalid_date = self.current_date + timedelta(days=1)
        form = BookingForm(data={'date': invalid_date.strftime('%Y-%m-%d')})
        self.assertFalse(form.is_valid(), 'Date must be at least 2 days ahead')

    def test_number_of_people_field_valid(self):
        """Test that the form is valid with a valid number of people (within allowed range)"""
        valid_data = self.valid_data.copy()
        valid_data['number_of_people'] = 5  # Valid input between 1 and 12
        form = BookingForm(data=valid_data)
        self.assertTrue(form.is_valid(),
                        'Form should be valid with a valid number of people')

    def test_number_of_people_field_invalid(self):
        """Test that the form is invalid if the number of people exceeds the max limit (12)"""
        invalid_data = self.valid_data.copy()
        # Invalid input (exceeds max of 12)
        invalid_data['number_of_people'] = 13
        form = BookingForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(), 'Form should be invalid if number of people exceeds 12')

    # Tests for empty fields

    def test_empty_date_field(self):
        """Ensure the form raises a validation error when date is empty"""
        invalid_data = self.valid_data.copy()
        invalid_data['date'] = ''  # Leave date empty
        form = BookingForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(), 'Form should be invalid with empty date')
        self.assertIn('date', form.errors,
                      'Form should raise an error for empty date')

    def test_empty_time_field(self):
        """Ensure the form raises a validation error when time is empty"""
        invalid_data = self.valid_data.copy()
        invalid_data['time'] = ''  # Leave time empty
        form = BookingForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(), 'Form should be invalid with empty time')
        self.assertIn('time', form.errors,
                      'Form should raise an error for empty time')

    def test_empty_number_of_people_field(self):
        """Ensure the form raises a validation error when number of people is empty"""
        invalid_data = self.valid_data.copy()
        invalid_data['number_of_people'] = ''  # Leave number_of_people empty
        form = BookingForm(data=invalid_data)
        self.assertFalse(
            form.is_valid(), 'Form should be invalid with empty number_of_people')
        self.assertIn('number_of_people', form.errors,
                      'Form should raise an error for empty number_of_people')
