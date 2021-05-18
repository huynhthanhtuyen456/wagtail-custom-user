from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (
    PasswordChangeView,
    PasswordResetView,
)
from drf_yasg.utils import swagger_auto_schema
# from rest_auth.views import LoginView
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from allauth.account.adapter import get_adapter
# from rest_framework.permissions import (IsAuthenticated)
# from django.conf import settings
from core.mails import send_confirm_code
from datetime import datetime, timedelta
import pytz
import string
import random

from core.tokens import account_activation_token
from . import serializers
from . import services
from .models import ConfirmCode, UserRole, User, UserSetting

from .serializers import (
    # SocialLoginSerializer,
    # SocialConnectSerializer,
    UserSettingSerializer
)


# class SocialConnectView(LoginView):
#     """
#     class used for social account linking
#     example usage for facebook with access_token
#     -------------
#     from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
#     class FacebookConnect(SocialConnectView):
#         adapter_class = FacebookOAuth2Adapter
#     -------------
#     """
#     serializer_class = SocialConnectSerializer  # override
#     permission_classes = (IsAuthenticated,)
#
#     def process_login(self):
#         get_adapter(self.request).login(self.request, self.user)


class ListUserRolesView(generics.ListAPIView):

    serializer_class = serializers.UserRoleSerializer

    def get_queryset(self):
        return UserRole.objects.all()


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserExistView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary='check exist email or username',
        operation_id='username_email_exist',
        security=[]
    )
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        email = request.query_params.get('email')

        exists = services.exists_user(username=username, email=email)
        data = {'exists': exists}
        return Response(data, status=status.HTTP_200_OK)


class SendConfirmCode(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '')

        if not email:
            error = {'email': 'Email is required'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        validate_email = User.objects.filter(email=email)
        if validate_email.exists():
            error = {'email': 'Email does not exist'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if validate_email.first().is_verified_email:
            error = {'email_conflict': ['The email has already been registered']}
            return Response(error, status=status.HTTP_409_CONFLICT)

        filter_code = ConfirmCode.objects.filter(email=email).first()
        if filter_code:
            filter_code.delete()

        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        email_status = send_confirm_code(email, code)

        confirm_code = ConfirmCode()
        confirm_code.code = code
        confirm_code.email = email
        confirm_code.expire_date = pytz.utc.localize(datetime.now() + timedelta(days=1))
        confirm_code.save()
        data = {'status': email_status}
        return Response(data, status=status.HTTP_200_OK)


class CompareConfirmCode(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        if not email:
            error = {'email': 'Email is required'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        validate_email = User.objects.filter(email=email)

        if validate_email.exists():
            error = {'email': 'Email does not exist'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if validate_email.first().is_verified_email:
            error = {'email_conflict': ['The email has already been registered']}
            return Response(error, status=status.HTTP_409_CONFLICT)

        try:
            confirm_code = ConfirmCode.objects.get(email=email, code=code)
        except ConfirmCode.DoesNotExist:
            error = {'confirm_code': 'Code invalid'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        now = pytz.utc.localize(datetime.now())
        if now > confirm_code.expire_date:
            error = {'confirm_code': 'Code invalid'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        data = {'status': 1}
        filter_code = ConfirmCode.objects.filter(email=email, code=code).first()
        if filter_code:
            filter_code.delete()

        validate_email.is_verified_email = True
        validate_email.is_active = True
        validate_email.save()

        return Response(data, status=status.HTTP_200_OK)


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
#     serializer_class = SocialLoginSerializer
#
#     @swagger_auto_schema(
#         operation_summary='Facebook login',
#         operation_id='facebook_login',
#         security=[]
#     )
#     def post(self, request, *args, **kwargs):
#         return super(FacebookLogin, self).post(request, *args, **kwargs)
#
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = settings.GOOGLE_CALLBACK_URL
#     client_class = OAuth2Client
#     serializer_class = SocialLoginSerializer
#
#     @swagger_auto_schema(
#         operation_summary='Google login',
#         operation_id='google_login',
#         security=[]
#     )
#     def post(self, request, *args, **kwargs):
#         return super(GoogleLogin, self).post(request, *args, **kwargs)


class UserSettingView(generics.CreateAPIView):
    serializer_class = UserSettingSerializer

    def create(self, request, *args, **kwargs):

        response = super().create(request)

        return response


class UserSettingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSettingSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return UserSetting.objects.filter(uuid=pk)
        return []


class UserVerifyEmailView(VerifyEmailView):
    pass


class UserPasswordChangeView(PasswordChangeView):
    pass


class UserPasswordResetView(PasswordResetView):
    pass


class ActivateAccountView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified_email = True
            user.save()
            messages.success(request, ('Your account have been confirmed.',))
            return render(request, "registration/success.html", {
                "user": user,
                "custom_title": "Registration Success"
            })
        else:
            messages.warning(request, ('The confirmation link was invalid,'
                                       ' possibly because it has already been used.'))
            # return redirect('login')
            return HttpResponseForbidden(content='The confirmation link was invalid,'
                                                 ' possibly because it has already been used.',
                                         content_type="text/html; charset=utf-8")