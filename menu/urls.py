from . import views
from django.urls import path

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu/delete-menu-item/<int:menu_item_id>', views.delete_menu_item, name ='delete_menu_item'),
    path('menu/edit-menu-item/<int:menu_item_id>', views.edit_menu_item, name ='edit_menu_item'),
]
