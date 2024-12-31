from . import views
from django.urls import path

urlpatterns = [
    path('book-table/', views.book_table, name='book_table'),
]
