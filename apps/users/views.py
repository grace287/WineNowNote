"""
인증 API (PRD 9.1)
- POST /api/auth/register — 회원가입
- POST /api/auth/login — 로그인 → tokens + user
- GET  /api/auth/me — 프로필 (JWT)
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """POST /api/auth/login"""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from django.contrib.auth import authenticate
        try:
            u = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("이메일 또는 비밀번호가 올바르지 않습니다.")
        user = authenticate(request, username=u.username, password=serializer.validated_data["password"])
        if not user:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed("이메일 또는 비밀번호가 올바르지 않습니다.")
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "tokens": tokens,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me — 현재 사용자 프로필"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
