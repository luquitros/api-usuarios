from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView


class LoginView(TokenObtainPairView):
    throttle_scope = 'login'


class LogoutView(TokenBlacklistView):
    throttle_scope = 'login'
