from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and hasattr(user, 'profile')
            and user.profile.user_type == 'admin'
        )


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if hasattr(user, 'profile') and user.profile.user_type == 'admin':
            return True

        if request.method in SAFE_METHODS or request.method in {'PUT', 'PATCH'}:
            return obj == user

        return False
