# users/models.py
from django.db import models
from django.contrib.auth import get_user_model

REGULAR = 'R'
ADMIN = 'A'
ROLE_CHOICES = [
    (REGULAR, 'Usuario regular'),
    (ADMIN, 'Administrador'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default=REGULAR,
        verbose_name='Rol'
    )
    
    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'
    
    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
    
    def is_admin(self):
        return self.role == ADMIN