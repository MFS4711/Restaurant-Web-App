from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
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
    
    # Handle Post request from Menu Item Form
    if request.method == "POST":
        menu_item_form = MenuItemForm(data=request.POST)
        if menu_item_form.is_valid():
            menu_item = menu_item_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New Menu Item Created'
            )
            # Redirect to menu page
            return redirect('menu')

    # Display form
    menu_item_form = MenuItemForm()

    context = {
        'categorised_items': categorised_items,
        'menu_item_form': menu_item_form,
    }

    return render(request, "menu/menu.html", context)
