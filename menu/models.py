from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class MenuItem(models.Model):
    """

    """
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('mains', 'Mains'),
        ('sides', 'Sides'),
        ('desserts', 'Desserts'),
        ('drinks', 'Drinks'),
    ]
    
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

    def __str__(self):
        return self.name