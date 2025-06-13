from rest_framework import serializers
from .models import Book, BorrowRecord
from users.models import UserProfile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRecordSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_email = serializers.CharField(source='user.user.email', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_title', 'user_email', 'borrow_date', 'return_date', 'returned']