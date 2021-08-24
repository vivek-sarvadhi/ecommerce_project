from rest_framework import permissions


class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == 1:
            return True
        return False


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == 2:
            return True
        return False