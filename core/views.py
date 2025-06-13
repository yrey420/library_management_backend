from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Book, BorrowRecord, UserProfile

class BookListView(ListView):
    model = Book
    template_name = 'core/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    
    def get_queryset(self):
        return Book.objects.filter(stock__gt=0).order_by('title')

class BookDetailView(DetailView):
    model = Book
    template_name = 'core/book_detail.html'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'core/book_form.html'
    fields = ['title', 'author', 'publication_year', 'stock']
    success_url = reverse_lazy('book-list')
    
    def test_func(self):
        return self.request.user.profile.is_admin()
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, 'Libro creado exitosamente!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'core/book_form.html'
    fields = ['title', 'author', 'publication_year', 'stock']
    success_url = reverse_lazy('book-list')
    
    def test_func(self):
        return self.request.user.profile.is_admin()
    
    def form_valid(self, form):
        messages.success(self.request, 'Libro actualizado exitosamente!')
        return super().form_valid(form)

class BorrowBookView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Book
    template_name = 'core/borrow_book.html'
    
    def test_func(self):
        # Solo usuarios regulares pueden pedir prestado
        return not self.request.user.profile.is_admin()
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user_profile = request.user.profile
        
        if book.stock <= 0:
            messages.error(request, 'No hay ejemplares disponibles de este libro.')
            return redirect('book-detail', pk=book.pk)
        
        # Verificar si el usuario ya tiene este libro prestado y no devuelto
        existing_borrow = BorrowRecord.objects.filter(
            user=user_profile,
            book=book,
            returned=False
        ).exists()
        
        if existing_borrow:
            messages.warning(request, 'Ya tienes este libro prestado.')
            return redirect('book-detail', pk=book.pk)
        
        # Crear el registro de préstamo
        BorrowRecord.objects.create(
            user=user_profile,
            book=book
        )
        
        # Reducir el stock
        book.stock -= 1
        book.save()
        
        messages.success(request, f'Has tomado prestado "{book.title}". ¡Disfrútalo!')
        return redirect('my-borrowed-books')

class ReturnBookView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BorrowRecord
    template_name = 'core/return_book.html'
    
    def test_func(self):
        # Solo el usuario que pidió prestado puede devolver
        borrow_record = self.get_object()
        return self.request.user.profile == borrow_record.user
    
    def post(self, request, *args, **kwargs):
        borrow_record = self.get_object()
        
        if borrow_record.returned:
            messages.warning(request, 'Este libro ya fue devuelto.')
            return redirect('my-borrowed-books')
        
        # Marcar como devuelto
        borrow_record.returned = True
        borrow_record.return_date = timezone.now()
        borrow_record.save()
        
        # Aumentar el stock
        book = borrow_record.book
        book.stock += 1
        book.save()
        
        messages.success(request, f'Has devuelto "{book.title}". ¡Gracias!')
        return redirect('my-borrowed-books')

class MyBorrowedBooksView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BorrowRecord
    template_name = 'core/my_borrowed_books.html'
    context_object_name = 'borrow_records'
    
    def test_func(self):
        # Solo usuarios regulares pueden ver sus préstamos
        return not self.request.user.profile.is_admin()
    
    def get_queryset(self):
        return BorrowRecord.objects.filter(
            user=self.request.user.profile,
        ).order_by('-borrow_date')