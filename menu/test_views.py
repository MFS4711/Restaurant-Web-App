from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import MenuItem


class TestMenuViews(TestCase):

    def setUp(self):
        """
        Set up a superuser and some test menu items for the following test
        cases.

        This method creates a superuser and several `MenuItem` objects that
        will be used across the tests to verify view behavior,
        such as creating, editing, and deleting menu items.
        """
        self.superuser = User.objects.create_superuser(
            username="superuser",
            password="password",
            email="superuser@test.com"
        )

        # Create some Mediterranean menu items for testing
        self.menu_item1 = MenuItem.objects.create(
            name="Kofta Kebab",
            description="Grilled spiced ground meat skewers",
            category="mains",
            price=10.00
        )
        self.menu_item2 = MenuItem.objects.create(
            name="Shawarma",
            description="Tender slices of spiced meat served in pita",
            category="mains",
            price=8.00
        )

    def test_menu_view(self):
        """
        Test that the menu view renders correctly with the expected context.

        This test ensures that the `menu` view loads the appropriate template,
        includes the `categorised_items` context variable, and correctly
        categorizes the menu items (e.g., into 'Mains' category).
        """
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu.html')

        # Verify that categorised_items is in the context
        self.assertIn('categorised_items', response.context)
        categorised_items = response.context['categorised_items']

        # Ensure categories contain the menu items
        mains_category = next(
            (items for label, items in categorised_items if label == 'Mains'),
            None
        )

        self.assertIsNotNone(mains_category)

        # Check that the expected menu items are in the correct categories
        self.assertTrue(self.menu_item1 in mains_category)
        self.assertTrue(self.menu_item2 in mains_category)

    def test_create_menu_item(self):
        """
        Test the creation of a new menu item by a superuser.

        This test verifies that a superuser can successfully create a new menu
        item via the `create_menu_item` view, that the user is redirected,
        and the correct success message is displayed.
        """
        self.client.login(username="superuser", password="password")
        url = reverse('create_menu_item', args=["Mains"])
        data = {
            'name': "Falafel",
            'description': "Crispy chickpea balls with tahini sauce",
            'category': "Mains",
            'price': 7.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('menu'))
        # Ensure the success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "New Menu Item Created")
        # Ensure the item was actually created
        self.assertTrue(MenuItem.objects.filter(
            name="Falafel").exists())

    def test_unauthorized_create_menu_item(self):
        """
        Test that a non-superuser cannot create a menu item.

        This test ensures that a non-superuser cannot create a new menu item
        and receives the appropriate error message indicating insufficient
        permissions.
        """
        # Create and log in a non-superuser
        self.client.login(username="superuser", password="password")
        non_superuser = User.objects.create_user(
            username="user", password="password")
        self.client.login(username="user", password="password")

        # Attempt to create a new menu item
        url = reverse('create_menu_item', args=["Mains"])
        data = {
            'name': "Hummus",
            'description': "Smooth and creamy chickpea dip",
            'category': "Mains",
            'price': 5.00
        }
        response = self.client.post(url, data)

        # Check that the response is a redirect with the error message
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('menu'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "You do not have permission to create menu items."
        )

        # Ensure the menu item was not created
        self.assertFalse(MenuItem.objects.filter(name="Hummus").exists())

    def test_edit_menu_item(self):
        """
        Test editing an existing menu item by a superuser.

        This test checks that a superuser can successfully edit an existing
        menu item, that the user is redirected after the edit, and that the
        correct success message is displayed.
        """
        self.client.login(username="superuser", password="password")
        url = reverse('edit_menu_item', args=[self.menu_item1.id])
        data = {
            'name': "Kofta Kebab Deluxe",
            'description': "Grilled spiced meat skewers with extra sauce",
            'category': "Mains",
            'price': 12.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('menu'))
        # Ensure the success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Menu Item Successfully Updated!")
        # Ensure the menu item was updated
        self.menu_item1.refresh_from_db()
        self.assertEqual(self.menu_item1.name, "Kofta Kebab Deluxe")

    def test_unauthorized_edit_menu_item(self):
        """
        Test that a non-superuser cannot edit a menu item.

        This test ensures that a non-superuser cannot edit an existing
        menu item and receives the appropriate error message indicating
        insufficient permissions.
        """
        # Create and log in a non-superuser
        self.client.login(username="superuser", password="password")
        non_superuser = User.objects.create_user(
            username="user", password="password")
        self.client.login(username="user", password="password")

        # Attempt to edit an existing menu item
        url = reverse('edit_menu_item', args=[self.menu_item1.id])
        data = {
            'name': "Kofta Kebab Supreme",
            'description': "Grilled spiced meat skewers with extra toppings",
            'category': "Mains",
            'price': 15.00
        }
        response = self.client.post(url, data)

        # Check that the response is a redirect with the error message
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('menu'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), "You do not have permission to edit menu items.")

        # Ensure the menu item was not updated
        self.menu_item1.refresh_from_db()
        self.assertNotEqual(self.menu_item1.name, "Kofta Kebab Supreme")

    def test_delete_menu_item(self):
        """
        Test deleting a menu item by a superuser.

        This test ensures that a superuser can delete a menu item successfully,
        the user is redirected, and the correct success message is shown
        after deletion.
        """
        self.client.login(username="superuser", password="password")
        url = reverse('delete_menu_item', args=[self.menu_item1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('menu'))
        # Ensure the success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Menu Item deleted!")
        # Ensure the item was deleted
        self.assertFalse(MenuItem.objects.filter(
            id=self.menu_item1.id).exists())

    def test_unauthorized_delete_menu_item(self):
        """
        Test that a non-superuser cannot delete a menu item.

        This test ensures that a non-superuser cannot delete a menu item and
        receives the appropriate error message indicating insufficient
        permissions.
        """
        # Create and log in a non-superuser
        self.client.login(username="superuser", password="password")
        non_superuser = User.objects.create_user(
            username="user", password="password")
        self.client.login(username="user", password="password")

        # Attempt to delete a menu item
        url = reverse('delete_menu_item', args=[self.menu_item1.id])
        response = self.client.post(url)

        # Check that the response is a redirect with the error message
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('menu'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "There was an error deleting the Item. Please try again."
        )

        # Ensure the item was not deleted
        self.assertTrue(MenuItem.objects.filter(
            id=self.menu_item1.id).exists())
