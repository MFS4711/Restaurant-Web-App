from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import MenuItem

# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('name', 'category', 'is_available', 'created_at', 'updated_at',)
    search_fields = ['name', 'category']
    list_filter = ('category',)


# admin.site.register(MenuItem)