from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    # image = CloudinaryFileField()

    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'image', 'price', 'is_available',)