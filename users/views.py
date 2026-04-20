from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import IsAdminOrSelf, IsAdminUserType
from .response import success_response
from .serializers import UserSerializer


class ApiHomeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Users API</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f3f6fb; color: #1f2937; margin: 0; }
    .wrap { max-width: 760px; margin: 48px auto; background: #fff; padding: 28px; border-radius: 14px; box-shadow: 0 8px 30px rgba(0,0,0,.08); }
    h1 { margin-top: 0; font-size: 28px; }
    p { line-height: 1.5; }
    .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 20px; }
    .card { border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; background: #fafafa; }
    a { color: #0f4c81; text-decoration: none; font-weight: 600; }
    code { background: #eef2f7; padding: 2px 5px; border-radius: 5px; }
  </style>
</head>
<body>
  <main class="wrap">
    <h1>Users API</h1>
    <p>Quick start for authentication and profile management.</p>
    <div class="cards">
      <section class="card">
        <h3>Documentation</h3>
        <p>Open API docs: <a href="/docs/">/docs/</a></p>
        <p>OpenAPI schema: <a href="/schema/">/schema/</a></p>
      </section>
      <section class="card">
        <h3>Auth Flow</h3>
        <p><code>POST /login/</code> to get tokens</p>
        <p><code>POST /refresh/</code> to refresh access</p>
        <p><code>POST /logout/</code> to blacklist refresh token</p>
      </section>
    </div>
    <p style="margin-top: 18px;">After login, call <code>GET /users/me/</code> with <code>Authorization: Bearer &lt;access&gt;</code>.</p>
  </main>
</body>
</html>
"""
        return HttpResponse(html)


@extend_schema_view(
    list=extend_schema(
        tags=['users'],
        summary='List users',
        description='Admin-only listing with pagination, search, filters, and ordering.',
    ),
    retrieve=extend_schema(tags=['users'], summary='Retrieve user'),
    create=extend_schema(
        tags=['users'],
        summary='Create user',
        description='Public signup endpoint.',
        examples=[
            OpenApiExample(
                'Signup',
                value={
                    'username': 'teacher',
                    'password': 'Teacher123!',
                    'email': 'teacher@example.com',
                    'first_name': 'Ada',
                    'last_name': 'Lovelace',
                    'profile': {
                        'user_type': 'professor',
                        'phone': '11999999999',
                        'bio': 'Math teacher',
                    },
                },
                request_only=True,
            ),
        ],
    ),
    update=extend_schema(tags=['users'], summary='Update user'),
    partial_update=extend_schema(tags=['users'], summary='Partial update user'),
    destroy=extend_schema(tags=['users'], summary='Delete user'),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['profile__user_type']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    ordering = ['id']

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginator = self.paginator
            data = {
                'items': serializer.data,
                'pagination': {
                    'count': paginator.page.paginator.count,
                    'next': paginator.get_next_link(),
                    'previous': paginator.get_previous_link(),
                    'page': paginator.page.number,
                    'page_size': paginator.get_page_size(request),
                },
            }
            return success_response(data=data, message='Users listed.')

        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message='Users listed.')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message='User retrieved.')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success_response(
            data=serializer.data,
            message='User created.',
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='User updated.')

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(data=None, message='User deleted.')

    @extend_schema(tags=['users'], summary='Current user profile')
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method.lower() == 'get':
            serializer = self.get_serializer(request.user)
            return success_response(data=serializer.data, message='Current user loaded.')

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Current user updated.')
