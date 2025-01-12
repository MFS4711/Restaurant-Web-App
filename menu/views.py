from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem
from .forms import MenuItemForm


def menu(request):
    """
    Display the menu page with all menu items grouped by categories.

    **Context:**

    ``categorised_items``
        A list of tuples where each tuple contains a category label and a
        queryset of MenuItems in that category.

    **Template:**

    :template:`menu/menu.html`
    """
    # Get all Menu Items from the database
    menu_items = MenuItem.objects.all()

    # Get distinct categories from the defined CATEGORY_CHOICES
    categories = MenuItem.CATEGORY_CHOICES

    # Create a list to store categories and their associated menu items
    categorised_items = []

    # Group menu items by category
    for category_value, category_label in categories:
        # Filter menu items by category
        category_items = menu_items.filter(category=category_value)
        categorised_items.append((category_label, category_items))

    # Pass the categorised menu items to the template context
    context = {
        'categorised_items': categorised_items,
    }

    # Render the menu template with the context
    return render(request, "menu/menu.html", context)


# Redirect to login if the user is not authenticated
@login_required(login_url='/accounts/login/')
def create_menu_item(request, category_label):
    """
    Handle the creation of a new menu item for a specific category.

    **Context:**

    ``menu_item_form``
        An instance of :form:`menu.MenuItemForm`
        used for creating a new menu item.

    ``category_label``
        The label of the category the new menu item belongs to.

    **Template:**

    :template:`menu/create_menu_item.html`
    """
    # Ensure only superusers can create menu items
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(
            request, 'You do not have permission to create menu items.')
        return redirect('menu')  # Redirect to the menu page if not authorized

    if request.method == "POST":
        # Initialize the form with POST data
        menu_item_form = MenuItemForm(data=request.POST)

        if menu_item_form.is_valid():
            # Set the category from the URL parameter
            menu_item = menu_item_form.save(commit=False)
            menu_item.category = category_label
            menu_item.save()

            # Display success message and redirect to the menu page
            messages.success(request, 'New Menu Item Created')
            return redirect('menu')  # Redirect to the menu page
        else:
            # If the form is not valid, show error message
            messages.error(request, 'Please correct the errors below.')

    else:
        # Instantiate an empty form for GET request
        menu_item_form = MenuItemForm()

    context = {
        'menu_item_form': menu_item_form,
        'category_label': category_label,
    }

    # Render the create menu item form template
    return render(request, "menu/create_menu_item.html", context)


# Redirect to login if the user is not authenticated
@login_required(login_url='/accounts/login/')
def edit_menu_item(request, menu_item_id):
    """
    Edit an existing menu item.

    **Context:**

    ``menu_item_form``
        An instance of :form:`menu.MenuItemForm`
        pre-filled with the details of the item being edited.

    ``menu_item``
        The menu item being edited.

    **Template:**

    :template:`menu/edit_menu_item.html`
    """
    # Ensure only superusers can edit menu items
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(
            request, 'You do not have permission to edit menu items.')
        return redirect('menu')  # Redirect to the menu page if not authorized

    # Retrieve the menu item to be edited, or return 404 if not found
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    if request.method == "POST":
        # Bind the form with POST data and pre-fill it with existing details
        menu_item_form = MenuItemForm(
            data=request.POST, files=request.FILES, instance=menu_item)

        if menu_item_form.is_valid():
            # Retain the current image if no new image is uploaded
            if not request.FILES.get('image'):
                menu_item_form.cleaned_data['image'] = menu_item.image
            menu_item_form.save()

            # Show success message and redirect to the menu page
            messages.success(request, 'Menu Item Successfully Updated!')
            return redirect('menu')
        else:
            # Display an error message if form validation fails
            messages.error(
                request, 'Error updating Menu Item. Please try again.')
    else:
        # Populate the form with current menu item details
        menu_item_form = MenuItemForm(instance=menu_item)

    context = {
        'menu_item_form': menu_item_form,
        'menu_item': menu_item,  # Pass the menu item to the template
    }

    # Render the edit menu item template
    return render(request, 'menu/edit_menu_item.html', context)


def delete_menu_item(request, menu_item_id):
    """
    Delete a menu item.

    **Context:**

    None

    **Template:**

    :template:`menu/menu.html`
    """
    # Ensure only superusers can delete menu items
    if not request.user.is_authenticated or not request.user.is_superuser:
        # Set the message for unauthorized users
        messages.error(
            request, 'There was an error deleting the Item. Please try again.')
        return redirect('menu')  # Redirect to the menu page if not authorized

    # Retrieve the menu item to delete, or return 404 if not found
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    # Perform the deletion
    menu_item.delete()  # Delete the menu item from the database
    messages.add_message(request, messages.SUCCESS, 'Menu Item deleted!')

    # Redirect to the menu page after deletion
    return redirect('menu')
