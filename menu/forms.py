from django import forms
from django.core.exceptions import ValidationError
from .models import MenuItem
import re


class MenuItemForm(forms.ModelForm):
    """
    A form for creating and updating MenuItem instances.

    This form is based on Django's ModelForm and is tied to the `MenuItem` model.
    It includes the following fields:

    - **name**: The name of the menu item.
    - **description**: A brief description of the menu item.
    - **image**: An image of the menu item (using Cloudinary).
    - **price**: The price of the menu item.
    - **is_available**: A boolean indicating if the item is available for sale.

    The form is used for both creating new menu items and updating existing ones.
    """

    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'image', 'price', 'is_available')

    # Define custom widget for the price field
    widgets = {
        'price': forms.NumberInput(attrs={
            'min': 0.01,  # Minimum price value (cannot be zero or negative)
            'step': '0.01',
            'placeholder': 'Enter price',  
            'class': 'form-control',
        }),
    }

    def clean_price(self):
        """
        Custom validation for the price field to ensure:
        1. The price is not 0 or None.
        2. The price is rounded to exactly two decimal places.

        If the validation fails, a ValidationError is raised with a corresponding message.
        """
        price = self.cleaned_data.get('price')

        # Check if the price is None or zero
        if price is None or price == 0:
            raise ValidationError("Price must be greater than 0.")

        # Round the price to exactly two decimal places to maintain consistency
        price = round(price, 2)

        # Validate that the price is represented as a float with exactly two decimal places
        # This regex ensures the price is in the correct format after rounding
        if not re.match(r'^\d+(\.\d{2})$', f'{price:.2f}'):
            raise ValidationError(
                "Price must have exactly two decimal places.")

        return price
