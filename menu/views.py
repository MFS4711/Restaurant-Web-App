from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
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
        # Retrieve the hidden category from the form submission
        category = request.POST.get('category')
        menu_item_form = MenuItemForm(data=request.POST)
        if menu_item_form.is_valid():
            menu_item = menu_item_form.save(commit=False)
            menu_item.category = category
            menu_item.save()
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
        menu_item_form = MenuItemForm(
            data=request.POST, files=request.FILES, instance=menu_item)
        if menu_item_form.is_valid():
            # Retain the current image if no new one is uploaded
            if not request.FILES.get('image'):
                menu_item_form.cleaned_data['image'] = menu_item.image
            menu_item_form.save()
            messages.success(request, 'Menu Item Successfully Updated!')
            return redirect('menu')
        else:
            messages.error(
                request, 'Error updating Menu Item. Please try again.')

    else:
        menu_item_form = MenuItemForm(instance=menu_item)
    
    context = {
        'menu_item_form': menu_item_form,
    }

    return render(request, 'menu.html', context)


def delete_menu_item(request, menu_item_id):
    """
    Delete a menu item.

    **Context:**

    None

    **Template:**

    :template:`menu/menu.html`
    """
    # get object you want to edit
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    if request.user.is_authenticated and (request.user.is_superuser):
        menu_item.delete()
        messages.add_message(request, messages.SUCCESS, 'Menu Item deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'There was an error deleting the Item. Please try again.')

    return HttpResponseRedirect(reverse('menu'))
