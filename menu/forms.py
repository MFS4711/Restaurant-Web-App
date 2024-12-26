from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    """
    A form for creating and updating MenuItem instances.

    This class uses Django's ModelForm to generate a form based on the MenuItem model. 
    It includes the following features:

    - **Model**: The form is tied to the `MenuItem` model.
    - **Fields**: The form includes the following fields:
      - `name`: The name of the menu item.
      - `description`: A brief description of the menu item.
      - `image`: An image of the menu item (currently commented out).
      - `price`: The price of the menu item.
      - `is_available`: A boolean indicating if the menu item is available for sale.
    
    This form is typically used in situations where administrators or staff can create or update menu items for a restaurant or café's menu.
    """

    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'image', 'price', 'is_available',)