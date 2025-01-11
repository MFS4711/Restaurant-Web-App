from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import MenuItem  

class MenuItemModelTest(TestCase):
    
    def setUp(self):
        """
        Create a test menu item to use in the tests.
        """
        self.menu_item = MenuItem.objects.create(
            name="Test Dish",
            description="A delicious test dish",
            price=Decimal('12.99'),
            category="mains",
            is_available=True
        )
    
    def test_menu_item_creation(self):
        """
        Test if the MenuItem is created properly.
        """
        self.assertEqual(self.menu_item.name, "Test Dish")
        self.assertEqual(self.menu_item.description, "A delicious test dish")
        self.assertEqual(self.menu_item.price, Decimal('12.99'))
        self.assertEqual(self.menu_item.category, "mains")
        self.assertTrue(self.menu_item.is_available)
    
    def test_default_values(self):
        """
        Test default values for a new MenuItem instance.
        """
        default_menu_item = MenuItem.objects.create(
            name="Default Dish",
            description="A default test dish",
            price=Decimal('9.99'),
        )
        
        self.assertEqual(default_menu_item.category, "starters")
        self.assertTrue(default_menu_item.is_available)
    
    def test_str_method(self):
        """
        Test the __str__ method of the MenuItem model.
        """
        self.assertEqual(str(self.menu_item), "Test Dish")
    
    def test_category_choices(self):
        """
        Test the valid category choices for a MenuItem.
        """
        valid_categories = [choice[0] for choice in MenuItem.CATEGORY_CHOICES]
        self.assertIn(self.menu_item.category, valid_categories)
    
    def test_invalid_category(self):
        """
        Test that an invalid category raises a ValidationError.
        """
        menu_item = MenuItem(
            name="Invalid Category Dish",
            description="A test dish with an invalid category",
            price=Decimal('10.99'),
            category="invalid_category",  # Invalid category
            is_available=True
        )
        
        # We expect a ValidationError to be raised
        with self.assertRaises(ValidationError):
            menu_item.full_clean()  # This triggers the validation process
    
    def test_menu_item_availability(self):
        """
        Test the availability of a MenuItem.
        """
        unavailable_item = MenuItem.objects.create(
            name="Unavailable Dish",
            description="This dish is unavailable",
            price=Decimal('5.99'),
            is_available=False
        )
        self.assertFalse(unavailable_item.is_available)
