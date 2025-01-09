from django.contrib import admin
from .models import MenuItem

# Register your models here.


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the MenuItem model.

    This class customizes the Django admin interface for the MenuItem model, providing the following features:

    - **List display**: Displays the 'name', 'category', 'is_available', 'created_at', and 'updated_at' fields in the admin list view.
    - **Search fields**: Allows searching by 'name' and 'category' in the admin search bar.
    - **List filters**: Adds filters for 'category' to narrow down the list of menu items.

    This class helps streamline the management of menu items in the admin panel, making it easier to manage and organize the items for a restaurant or café menu.
    """
    list_display = ('name', 'category', 'is_available',
                    'created_at', 'updated_at',)
    search_fields = ['name', 'category']
    list_filter = ('category',)
