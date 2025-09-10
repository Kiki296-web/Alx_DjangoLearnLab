# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods for anyone, but only owners can modify/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write allowed only to author/owner
        try:
            return obj.author == request.user
        except AttributeError:
            # If object doesn't have author attr, deny
            return False
