from rest_framework import permissions

from .models import CustomUser


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_staff
                     or request.user.role == CustomUser.UserRole.ADMIN)
                )


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_staff
                     or request.user.role == CustomUser.UserRole.ADMIN)
                or request.method in permissions.SAFE_METHODS)


class ReviewOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == CustomUser.UserRole.MODERATOR)
