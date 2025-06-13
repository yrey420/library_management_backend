from rest_framework.permissions import BasePermission
from users.models import UserProfile

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == UserProfile.ADMIN

class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == UserProfile.REGULAR