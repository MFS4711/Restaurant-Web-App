from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


class MenuItem(models.Model):
    """
    Represents a menu item in a restaurant or food service application.

    This model stores the details of a menu item,
    including its name, description,
    associated image, category
    (e.g., starters, mains, sides, desserts, drinks),
    price, and availability status.

    Attributes:
        name (str): The name of the menu item.
        description (str): A detailed description of the menu item.
        image (CloudinaryField): An image associated with the menu item,
        stored in Cloudinary.
        category (str): The category of the menu item,
        chosen from predefined categories (e.g., 'starters', 'mains', etc.).
        price (Decimal): The price of the menu item.
        is_available (bool): A boolean indicating whether the item is available

    Methods:
        __str__(): Returns the name of the menu item.
    """

    # Define the choices for categories of menu items
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('mains', 'Mains'),
        ('sides', 'Sides'),
        ('desserts', 'Desserts'),
        ('drinks', 'Drinks'),
    ]

    # Fields of the MenuItem model
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image', default='placeholder')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='starters',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the name of the menu item when the object is printed.
        """
        return self.name
