# core/models.py
from django.db import models
from django.core.validators import MinValueValidator
from users.models import UserProfile

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    author = models.CharField(max_length=100, verbose_name='Autor')
    publication_year = models.PositiveIntegerField(
        verbose_name='Año de publicación',
        validators=[MinValueValidator(1000)]
    )
    stock = models.PositiveIntegerField(
        verbose_name='Cantidad en stock',
        default=1
    )
    
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['title']
    
    def __str__(self):
        return f'{self.title} ({self.author}, {self.publication_year})'

class BorrowRecord(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    borrow_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de préstamo'
    )
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de devolución'
    )
    returned = models.BooleanField(
        default=False,
        verbose_name='Devuelto'
    )
    
    class Meta:
        verbose_name = 'Registro de préstamo'
        verbose_name_plural = 'Registros de préstamo'
        ordering = ['-borrow_date']
    
    def __str__(self):
        status = "devuelto" if self.returned else "prestado"
        return f'{self.book.title} {status} por {self.user.user.username}'