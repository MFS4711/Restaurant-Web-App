from decimal import Decimal

from django.test import TestCase

from .forms import MenuItemForm


class TestMenuItemForm(TestCase):

    def test_form_is_valid(self):
        """
        Test that the form is valid with correct data.

        This test ensures that when valid data is provided for all required fields 
        (name, description, price, and availability), the form is considered valid.
        """
        valid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': 5.99,
            'is_available': True,
        }
        form = MenuItemForm(valid_data)
        self.assertTrue(form.is_valid(), msg='Form is invalid with valid data')

    def test_form_is_invalid_empty_name(self):
        """
        Test that the form is invalid when the name field is empty.

        This test ensures that the form does not pass validation when the required 
        `name` field is left empty.
        """
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
        """
        Test that the form is invalid when the price is zero.

        This test checks that the form does not accept a price of zero, which 
        is an invalid value for menu item pricing.
        """
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
        """
        Test that the form is invalid when the price is None.

        This test ensures that the form does not accept `None` as a valid price, 
        which is an invalid entry for the price field.
        """
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
        """
        Test that the form is valid when the price has exactly two decimal places.

        This test checks that the form accepts a valid price with exactly two decimal places,
        which is the expected format for the price.
        """
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
        """
        Test that the form is invalid when the price has more than two decimal places.

        This test ensures that the form rejects a price with more than two decimal places, 
        as this is considered an invalid format for the price.
        """
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': Decimal('5.999'),
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(form.is_valid(),
                         msg='Form is valid with price having more than two decimal places')

    def test_form_is_invalid_with_non_numeric_price(self):
        """
        Test that the form is invalid when the price is a non-numeric value.

        This test verifies that the form rejects a non-numeric value (such as a string) 
        for the price field, ensuring that only valid numeric values are accepted.
        """
        invalid_data = {
            'name': 'Hummus',
            'description': 'A creamy and flavorful hummus',
            'price': 'invalid',
            'is_available': True,
        }
        form = MenuItemForm(invalid_data)
        self.assertFalse(
            form.is_valid(), msg='Form is valid with non-numeric price')
