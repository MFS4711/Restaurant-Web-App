from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Table, Booking

# Register your models here.

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available')
    search_fields = ('table_number',)
    list_filter = ('is_available',)
    ordering = ('table_number',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'date', 'time', 'number_of_people', 'status', 'table', 'created_at', 'updated_at'
    )
    search_fields = ('status',)
    list_filter = ('status', 'date', 'table')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'table')