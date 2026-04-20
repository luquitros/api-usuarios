from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .response import success_response


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LoginView(TokenObtainPairView):
    throttle_scope = 'login'

    @extend_schema(
        tags=['auth'],
        summary='Login',
        request=LoginRequestSerializer,
        examples=[
            OpenApiExample(
                'Login example',
                value={'username': 'teacher', 'password': 'Teacher123!'},
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data, message='Login successful.', status_code=response.status_code)


class LogoutView(TokenBlacklistView):
    throttle_scope = 'login'

    @extend_schema(
        tags=['auth'],
        summary='Logout',
        request=LogoutRequestSerializer,
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=None, message='Logout successful.', status_code=response.status_code)


class RefreshView(TokenRefreshView):
    @extend_schema(
        tags=['auth'],
        summary='Refresh access token',
        request=RefreshRequestSerializer,
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response(data=response.data, message='Token refreshed.', status_code=response.status_code)
