from django.urls import path
from . import views

# URL patterns for the menu-related views
urlpatterns = [
    # View to display the menu
    path('menu/', views.menu, name='menu'),

    # View to create a new menu item
    path('menu/create-menu-item/<str:category_label>/', views.create_menu_item, name='create_menu_item'),

    # View to delete a specific menu item
    path('menu/delete-menu-item/<int:menu_item_id>/',
         views.delete_menu_item, name='delete_menu_item'),

    # View to edit a specific menu item
    path('menu/edit-menu-item/<int:menu_item_id>/',
         views.edit_menu_item, name='edit_menu_item'),
]