from rest_framework.permissions import SAFE_METHODS, BasePermission


def _is_api_admin(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return hasattr(user, 'profile') and user.profile.user_type == 'admin'


class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        return _is_api_admin(request.user)


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if _is_api_admin(user):
            return True

        if request.method in SAFE_METHODS or request.method in {'PUT', 'PATCH'}:
            return obj == user

        return False
