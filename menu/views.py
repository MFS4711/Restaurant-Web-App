from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
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
    view to edit a item
    """
    # get object you want to edit
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    if request.method == "POST":
        # iniitialises form with instance of MenuItem pre-filled
        menu_item_form = MenuItemForm(data=request.POST, files=request.FILES, instance=menu_item)
        # form validation and authentication check
        if menu_item_form.is_valid():
            # save the form with updated data
            menu_item = menu_item_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Menu Item Successfully Updated!')
            # Redirect to menu page
            return redirect('menu')
        else:
            messages.add_message(
                request, messages.ERROR, 'There was an error updating the Menu Item. Please try again.')
    
    else:
        menu_item_form = MenuItemForm(instance=menu_item)

    # Below with the view to run - and in args - the necessary parameter (if applicable)
    return HttpResponseRedirect(reverse('menu'))

def delete_menu_item(request, menu_item_id):
    """
    view to delete a item
    """
    # get object you want to edit
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)

    if request.user.is_authenticated and (request.user.is_superuser):
        menu_item.delete()
        messages.add_message(request, messages.SUCCESS, 'Menu Item deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'There was an error deleting the Item. Please try again.')

    return HttpResponseRedirect(reverse('menu'))