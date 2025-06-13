from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BorrowBookView,
    ReturnBookView,
    MyBorrowedBooksView,
)

app_name = 'core'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/add/', BookCreateView.as_view(), name='book-add'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book-edit'),
    path('book/<int:pk>/borrow/', BorrowBookView.as_view(), name='book-borrow'),
    path('borrow/<int:pk>/return/', ReturnBookView.as_view(), name='book-return'),
    path('my-books/', MyBorrowedBooksView.as_view(), name='my-borrowed-books'),
]