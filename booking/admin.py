from django.contrib import admin
from .models import Table, Booking

# Register your models here.


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Table model.

    This class customizes the Django admin interface for the Table model,
    providing the following features:

    - **List display**: Displays the 'table_number', 'capacity', and
    'is_available' fields in the admin list view.
    - **Search fields**: Allows searching by 'table_number'
    in the admin search bar.
    - **List filters**: Adds a filter for 'is_available' to narrow down
    the list of tables.
    - **Ordering**: Orders the tables by 'table_number' in ascending order
    in the admin list.

    This class helps streamline the management of tables in a restaurant or
    venue, making it easier to track available and occupied tables.
    """
    list_display = ('table_number', 'capacity', 'is_available')
    search_fields = ('table_number',)
    list_filter = ('is_available',)
    ordering = ('table_number',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Booking model.

    This class customizes the Django admin interface for the Booking model,
    providing the following features:

    - **List display**: Displays the 'user', 'date', 'time',
    'number_of_people', 'status', 'table', 'created_at', and 'updated_at'
    fields in the admin list view.
    - **Search fields**: Allows searching by 'status' in the admin search bar.
    - **List filters**: Adds filters for 'status', 'date', and 'table' to
    narrow down the list of bookings.
    - **Ordering**: Orders the bookings by 'created_at' in descending order.
    - **Read-only fields**: Makes the 'created_at' and 'updated_at' fields
    read-only in the admin interface.
    - **List editable**: Allows 'status' and 'table' fields to be edited
    directly in the admin list view for quicker updates.

    This class helps streamline the management of bookings in the admin panel,
    making it easier to track and modify booking details.
    """
    list_display = (
        'user', 'date', 'time', 'number_of_people',
        'status', 'table', 'created_at', 'updated_at'
    )
    search_fields = ('status',)
    list_filter = ('status', 'date', 'table')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'table')
