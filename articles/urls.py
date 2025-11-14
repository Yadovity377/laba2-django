# articles/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('books/', views.books_list, name='books_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books/delete/', views.delete_book, name='delete_book'),
    path('books/delete-db/<int:pk>/', views.delete_book_db, name='delete_book_db'),
    path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('books/search/', views.book_search, name='book_search'),
]