from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import MenuItem


class MenuItemModelTest(TestCase):

    def setUp(self):
        """
        Set up a test instance of MenuItem to be used in the following
        test cases.

        This method creates a `MenuItem` object that will be available for
        all test methods to ensure consistent data across tests.
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
        Test that a MenuItem object is correctly created and its fields
        match the given data.

        This test ensures that the attributes like `name`, `description`,
        `price`, `category`, and `is_available` are properly set during
        the object creation.
        """
        self.assertEqual(self.menu_item.name, "Test Dish")
        self.assertEqual(self.menu_item.description, "A delicious test dish")
        self.assertEqual(self.menu_item.price, Decimal('12.99'))
        self.assertEqual(self.menu_item.category, "mains")
        self.assertTrue(self.menu_item.is_available)

    def test_default_values(self):
        """
        Test that a new MenuItem instance uses the correct default values
        for fields not explicitly set.

        This test checks the behavior when a `MenuItem` is created without
        specifying certain fields, ensuring that defaults like `category`
        and `is_available` are set properly.
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
        Test the `__str__` method of the MenuItem model.

        The `__str__` method should return a string representation of the
        MenuItem based on the `name` field. This test ensures that the method
        returns the expected string when called on a MenuItem instance.
        """
        self.assertEqual(str(self.menu_item), "Test Dish")

    def test_category_choices(self):
        """
        Test that the `category` field of the MenuItem model only allows
        valid choices.

        The `category` field should be one of the values defined in the
        `CATEGORY_CHOICES`.
        This test validates that the instance's `category` is one of
        those choices.
        """
        valid_categories = [choice[0] for choice in MenuItem.CATEGORY_CHOICES]
        self.assertIn(self.menu_item.category, valid_categories)

    def test_invalid_category(self):
        """
        Test that an invalid category raises a `ValidationError`.

        When an invalid category (not in the defined `CATEGORY_CHOICES`) is set
        for a `MenuItem`, a `ValidationError` should be raised when the
        object is validated.
        """
        menu_item = MenuItem(
            name="Invalid Category Dish",
            description="A test dish with an invalid category",
            price=Decimal('10.99'),
            category="invalid_category",
            is_available=True
        )

        # Expect a ValidationError to be raised due to an invalid category
        with self.assertRaises(ValidationError):
            menu_item.full_clean()

    def test_menu_item_availability(self):
        """
        Test that the `is_available` field of a MenuItem correctly reflects the
        availability.

        This test checks whether a MenuItem's `is_available` flag can be set to
        `False`, indicating that it is not available for ordering.
        """
        unavailable_item = MenuItem.objects.create(
            name="Unavailable Dish",
            description="This dish is unavailable",
            price=Decimal('5.99'),
            is_available=False
        )
        self.assertFalse(unavailable_item.is_available)
