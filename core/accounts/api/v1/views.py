from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# from django.core.mail import send_mail
from django.conf import settings

from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.state import api_settings

from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from accounts.models import Profile
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from ..utils import SendThreadingEmailMessage


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {"email": serializer.validated_data["email"]}

        # user = get_object_or_404(User, email=data.get('email'))
        token = self.get_token_for_user(user)
        email_obj = EmailMessage(
            "email/email_activation.tpl",
            {
                "token": token,
            },
            "admin@admin.admin",
            to=[user.email],
        )
        SendThreadingEmailMessage(email_obj).start()

        return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, user):
        access_token = AccessToken()
        # token = access_token.for_user(user)
        access_token.payload["user_id"] = user.pk
        access_token.payload["email"] = user.email
        return str(access_token)


class ActivationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM]
            )
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "Token is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"detail": "Token is not valid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=user_id)
        if user.is_verified:
            return Response(
                {"detail": "Your account is already verified and activated."},
                status=status.HTTP_202_ACCEPTED,
            )
        user.is_verified = True
        user.is_active = True
        user.save()

        return Response(
            {
                "detail": "Your account has been verified and activated successfully."
            },
            status=status.HTTP_200_OK,
        )


class ActivationResendAPIView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_token_for_user(user)
        email_obj = EmailMessage(
            "email/email_activation.tpl",
            {
                "token": token,
            },
            "admin@admin.admin",
            to=[user.email],
        )
        SendThreadingEmailMessage(email_obj).start()
        return Response(
            {"detail": "User activation resend link sent successfully."},
            status=status.HTTP_200_OK,
        )

    def get_token_for_user(self, user):
        access_token = AccessToken()
        # token = access_token.for_user(user)
        access_token.payload["user_id"] = user.pk
        access_token.payload["email"] = user.email
        return str(access_token)


class ChangePasswordAPIView(GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # serializer.errors, status=400(BadRequest)

        if not self.object.check_password(serializer.data.get("old_password")):
            return Response(
                {"old_password": "Wrong password!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class ProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestSendEmail(APIView):
    def get(self, request, *args, **kwargs):
        user_email = "test@test.test"
        user = get_object_or_404(User, email=user_email)
        token = self.get_token_for_user(user)

        email_obj = EmailMessage(
            "email/hello.tpl",
            {
                "name": "Amir",
                "token": token,
            },
            "admin@admin.admin",
            to=[user_email],
        )
        SendThreadingEmailMessage(email_obj).start()
        return Response("Email sent.")

    def get_token_for_user(self, user):
        token = AccessToken.for_user(user)
        return str(token)
