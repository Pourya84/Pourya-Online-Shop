from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "customer"):
            return obj.customer == request.user.profile

        return obj.id == request.user.profile.id


class IsSellerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.profile.role == "seller"


class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.seller == request.user.profile
