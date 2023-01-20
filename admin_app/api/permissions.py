from rest_framework import permissions

class AdminUserOrWriteOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in 'POST':
            return True
        else:
            return request.user and request.user.is_staff