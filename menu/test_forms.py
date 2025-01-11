from django.test import TestCase
from .forms import MenuItemForm
from decimal import Decimal


class TestMenuItemForm(TestCase):

    def test_form_is_valid(self):
        # Valid data for the form
        valid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': 5.99,
            'is_available': True,
        }
        form = MenuItemForm(valid_data)
        self.assertTrue(form.is_valid(), msg='Form is invalid with valid data')

    def test_form_is_invalid_empty_name(self):
        # Invalid data: name is empty
        invalid_data = {
            'name': '',
            'description': 'A creamy and flavorful hummus',
            'price': 5.99,
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(
            form.is_valid(), msg='Form is valid when name is empty')

    def test_form_is_invalid_zero_price(self):
        # Invalid data: price is zero
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': 0,
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(
            form.is_valid(), msg='Form is valid when price is zero')

    def test_form_is_invalid_none_price(self):
        # Invalid data: price is None
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': None,
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(
            form.is_valid(), msg='Form is valid when price is None')

    def test_form_is_valid_with_two_decimal_places(self):
        # Valid data: price with exactly two decimal places
        valid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': Decimal('5.99'),
            'is_available': True,
        }
        form = MenuItemForm(valid_data)
        self.assertTrue(
            form.is_valid(), msg='Form is invalid with price having two decimal places')

    def test_form_is_invalid_with_more_than_two_decimal_places(self):
        # Invalid data: price with more than two decimal places
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': Decimal('5.999'),
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(form.is_valid(
        ), msg='Form is valid with price having more than two decimal places')

    def test_form_is_invalid_with_non_numeric_price(self):
        # Invalid data: price with a non-numeric value
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': 'invalid',
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(
            form.is_valid(), msg='Form is valid with non-numeric price')
