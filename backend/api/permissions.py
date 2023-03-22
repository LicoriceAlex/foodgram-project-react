from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedOrListOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class IsAuthorOrAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user