from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminOrSelf, IsAdminUserType


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        queryset = User.objects.select_related('profile').all()
        if hasattr(user, 'profile') and user.profile.user_type == 'admin':
            return queryset

        return queryset.filter(id=user.id)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in {'list', 'destroy'}:
            permission_classes = [IsAdminUserType]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrSelf]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method.lower() == 'get':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
