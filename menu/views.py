from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import MenuItem
from .forms import MenuItemForm


def menu(request):
    """
    Display the menu page with all menu items grouped by categories.

    **Context:**

    ``categorised_items``
        A list of tuples where each tuple contains a category label and a queryset of MenuItems in that category.
    ``menu_item_form``
        An instance of :form:`menu.MenuItemForm` to add a new menu item.

    **Template:**

    :template:`menu/menu.html`
    """
    # Get all Menu Items
    menu_items = MenuItem.objects.all()

    # Get distinct categories from the defined CATEGORY_CHOICES
    categories = MenuItem.CATEGORY_CHOICES

    # Create a list to store categories and their associated items
    categorised_items = []

    for category_value, category_label in categories:
        # Filter menu items by category
        category_items = menu_items.filter(category=category_value)
        categorised_items.append((category_label, category_items))

    # Handle POST request from the Menu Item Form
    if request.method == "POST":
        menu_item_form = MenuItemForm(data=request.POST)

        # Check if the form is valid
        if menu_item_form.is_valid():
            # Get category from the form data
            category = request.POST.get('category')
            menu_item = menu_item_form.save(commit=False)
            menu_item.category = category  # Set the category manually
            menu_item.save()
            messages.add_message(request, messages.SUCCESS,
                                 'New Menu Item Created')
            return redirect('menu')  # Redirect to the menu page
        else:
            messages.error(request, 'Please correct the errors below.')

    # Display empty form for new menu item
    else:
        menu_item_form = MenuItemForm()

    context = {
        'categorised_items': categorised_items,
        'menu_item_form': menu_item_form,
    }

    return render(request, "menu/menu.html", context)


def edit_menu_item(request, menu_item_id):
    """
    Edit an existing menu item.

    **Context:**

    ``menu_item_form``
        An instance of :form:`menu.MenuItemForm` pre-filled with the details of the item being edited.

    **Template:**

    :template:`menu/menu.html`
    """
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    if request.method == "POST":
        # Bind form with POST data and pre-fill with existing menu item details
        menu_item_form = MenuItemForm(
            data=request.POST, files=request.FILES, instance=menu_item)

        # Check if form is valid
        if menu_item_form.is_valid():
            # Retain current image if no new image is uploaded
            if not request.FILES.get('image'):
                menu_item_form.cleaned_data['image'] = menu_item.image
            menu_item_form.save()
            messages.success(request, 'Menu Item Successfully Updated!')
            return redirect('menu')
        else:
            messages.error(
                request, 'Error updating Menu Item. Please try again.')

    else:
        # Populate the form with the current menu item details
        menu_item_form = MenuItemForm(instance=menu_item)

    context = {
        'menu_item_form': menu_item_form,
    }

    return render(request, 'menu/menu.html', context)


def delete_menu_item(request, menu_item_id):
    """
    Delete a menu item.

    **Context:**

    None

    **Template:**

    :template:`menu/menu.html`
    """
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    # Check if the user is authenticated and a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        menu_item.delete()
        messages.add_message(request, messages.SUCCESS, 'Menu Item deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'There was an error deleting the Item. Please try again.')

    return redirect('menu')  # Redirect to the menu page after deletion
