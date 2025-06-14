from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from core.models import Book, BorrowRecord
from core.api.serializers import BookSerializer, BorrowRecordSerializer
from core.permissions import IsAdmin, IsRegularUser

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return []

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsRegularUser])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user_profile = request.user.profile

        if book.stock <= 0:
            return Response({"error": "No hay ejemplares disponibles"}, status=status.HTTP_400_BAD_REQUEST)

        if BorrowRecord.objects.filter(user=user_profile, book=book, returned=False).exists():
            return Response({"error": "Ya tienes este libro prestado"}, status=status.HTTP_400_BAD_REQUEST)

        BorrowRecord.objects.create(user=user_profile, book=book)
        book.stock -= 1
        book.save()

        return Response({"success": f"Libro '{book.title}' prestado"}, status=status.HTTP_201_CREATED)

class BorrowRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return BorrowRecord.objects.filter(user=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        record = self.get_object()

        if record.returned:
            return Response({"error": "Este libro ya fue devuelto"}, status=status.HTTP_400_BAD_REQUEST)

        record.returned = True
        record.return_date = timezone.now()
        record.save()

        book = record.book
        book.stock += 1
        book.save()

        return Response({"success": f"Libro '{book.title}' devuelto"}, status=status.HTTP_200_OK)