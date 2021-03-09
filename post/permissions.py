from rest_framework.permissions import BasePermission


class IsPostAuthor(BasePermission):
    """
    Permission to check whether the user is the author of the post.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
