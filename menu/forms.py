from django import forms
from .models import MenuItem

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