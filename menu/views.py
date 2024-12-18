from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import MenuItem
from .forms import MenuItemForm

def homepage(request):
    """

    """

    return render(request, "menu/index.html")

def menu(request):
    """

    """

    # Get all Menu Items
    menu_items = MenuItem.objects.all()

    # get distinct categories
    categories = MenuItem.CATEGORY_CHOICES

    # Create a list to store categories and their items
    categorised_items = []
    
    for category_value, category_label in categories:
        # Get menu items for the current category
        category_items = menu_items.filter(category=category_value)
        categorised_items.append((category_label, category_items))

    # Display form
    menu_item_form = MenuItemForm

    context = {
        'categorised_items': categorised_items,
        'menu_item_form': menu_item_form,
    }

    return render(request, "menu/menu.html", context)
