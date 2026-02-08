
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        # Adjust this based on your model field name (owner, user, author, etc.)
        return obj.user == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only for everyone, but write only for admin users.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff

class IsOwner(permissions.BasePermission):
    """
    Only allow owners to access their own objects.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user