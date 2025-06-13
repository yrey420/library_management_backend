from django.contrib import admin
from .models import Book, UserProfile, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'stock')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'return_date', 'returned')
    list_filter = ('returned', 'borrow_date')
    search_fields = ('book__title', 'user__user__username')