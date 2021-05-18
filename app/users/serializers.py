from rest_framework import serializers, exceptions
from rest_auth.registration.serializers import RegisterSerializer as RestAuthRegisterSerializer
from rest_auth.serializers import PasswordResetSerializer as RestAuthPasswordResetSerializer
from rest_auth.registration.serializers import SocialLoginSerializer as RestSocialLoginSerializer, SocialConnectMixin
from allauth.socialaccount.helpers import complete_social_login
from allauth.account import app_settings as allauth_settings
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from rest_framework.authtoken.models import Token
from users.forms import PasswordResetForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from requests.exceptions import HTTPError

from .models import User, UserRole, UserSetting


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('pk', 'role')


class UserProfileSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        return ret

    class InnerRole(serializers.ModelSerializer):
        class Meta:
            model = UserRole
            fields = ('pk', 'role')

    class Meta:
        model = User
        fields = ('user_id', 'phone_number', 'profile_video_url',
                  'proof_of_identification_url', 'avatar_url', 'youtube_url', 'role', 'name', 'first_name', 'last_name',
                  'email', 'is_verified_email')

    role = InnerRole(many=False, read_only=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    role_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=UserRole.objects.all(),
                                                 source='role')

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class RegisterSerializer(RestAuthRegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=False, default=None)
    last_name = serializers.CharField(max_length=150, required=False, default=None)
    phone_number = serializers.CharField(max_length=15, required=False, default=None)
    is_verified_email = serializers.BooleanField(default=False)
    profile_video_url = serializers.FileField(required=False, default=None)
    proof_of_identification_url = serializers.FileField(required=False)
    avatar_url = serializers.ImageField(required=False, default=None)
    youtube_url = serializers.CharField(max_length=255, required=False, default=None)

    def get_cleaned_data(self):
        clean_data = super(RegisterSerializer, self).get_cleaned_data()
        clean_data.update({
            'first_name': self.validated_data.get('first_name', None),
            'last_name': self.validated_data.get('last_name', None),
            'phone_number': self.validated_data.get('phone_number', None),
            'is_verified_email': self.validated_data.get('is_verified_email', False),
            'profile_video_url': self.validated_data.get('profile_video_url', None),
            'proof_of_identification_url': self.validated_data.get('proof_of_identification_url', None),
            'avatar_url': self.validated_data.get('avatar_url', None),
            'youtube_url': self.validated_data.get('youtube_url', None)
        })
        return clean_data

    def custom_signup(self, request, user):
        user.phone_number = self.validated_data.get('phone_number')
        user.is_verified_email = self.validated_data.get('is_verified_email')
        user.profile_video_url = self.validated_data.get('profile_video_url')
        user.proof_of_identification_url = self.validated_data.get('proof_of_identification_url')
        user.avatar_url = self.validated_data.get('avatar_url')
        user.youtube_url = self.validated_data.get('youtube_url')
        user.save()


class PasswordResetSerializer(RestAuthPasswordResetSerializer):
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        value = super(PasswordResetSerializer, self).validate_email(value)
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "We couldn't find a FinSC account associated with %s" % value)
        return value

    def get_email_options(self):
        return {
            'subject_template_name': 'registration/password_reset_subject.txt',
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': {
                "frontend_url": settings.FRONTEND_BASE_URL
            }
        }


# class SocialLoginSerializer(RestSocialLoginSerializer):  # override
#     def validate(self, attrs):
#         view = self.context.get('view')
#         request = self._get_request()
#
#         if not view:
#             raise serializers.ValidationError(
#                 _("View is not defined, pass it as a context variable")
#             )
#
#         adapter_class = getattr(view, 'adapter_class', None)
#         if not adapter_class:
#             raise serializers.ValidationError(_("Define adapter_class in view"))
#
#         adapter = adapter_class(request)
#         app = adapter.get_provider().get_app(request)
#
#         # More info on code vs access_token
#         # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token
#
#         # Case 1: We received the access_token
#         if attrs.get('access_token'):
#             access_token = attrs.get('access_token')
#
#         # Case 2: We received the authorization code
#         elif attrs.get('code'):
#             self.callback_url = getattr(view, 'callback_url', None)
#             self.client_class = getattr(view, 'client_class', None)
#
#             if not self.callback_url:
#                 raise serializers.ValidationError(
#                     _("Define callback_url in view")
#                 )
#             if not self.client_class:
#                 raise serializers.ValidationError(
#                     _("Define client_class in view")
#                 )
#
#             code = attrs.get('code')
#
#             provider = adapter.get_provider()
#             scope = provider.get_scope(request)
#             client = self.client_class(
#                 request,
#                 app.client_id,
#                 app.secret,
#                 adapter.access_token_method,
#                 adapter.access_token_url,
#                 self.callback_url,
#                 scope
#             )
#             token = client.get_access_token(code)
#             access_token = token['access_token']
#
#         else:
#             raise serializers.ValidationError(
#                 _("Incorrect input. access_token or code is required."))
#
#         social_token = adapter.parse_token({'access_token': access_token})
#         social_token.app = app
#         try:
#             login = self.get_social_login(adapter, app, social_token, access_token)
#             complete_social_login(request, login)
#
#         except HTTPError:
#             raise serializers.ValidationError(_("Incorrect value"))
#
#         if not login.is_existing:
#             # We have an account already signed up in a different flow
#             # with the same email address: raise an exception.
#             # This needs to be handled in the frontend. We can not just
#             # link up the accounts due to security constraints
#             if not allauth_settings.UNIQUE_EMAIL:
#                 # Do we have an account already with this email address?
#                 account_exists = get_user_model().objects.filter(
#                     email=login.user.email,
#                 ).exists()
#                 if account_exists:
#                     raise serializers.ValidationError(
#                         _("User is already registered with this e-mail address.")
#                     )
#
#             login.lookup()
#             login.save(request, connect=True)
#
#         if login.user != request.user:
#             """
#             custom
#             case: two accounts connect to the same social account, switch that social account to the last connecting
#             """
#             social_account = SocialAccount.objects.filter(uid=login.account.uid).first()
#             social_account.user = request.user
#             social_account.save()
#             attrs['user'] = request.user
#             return attrs
#
#         Token.objects.filter(user=login.account.user).delete()
#
#         attrs['user'] = login.account.user
#
#         return attrs
#
#
# class SocialConnectSerializer(SocialConnectMixin, SocialLoginSerializer):
#     """
#     custom Social Connect Serializer
#     it is inherited from SocialLoginSerializer and it is also override above
#     """
#     pass


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        elif username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        Token.objects.filter(user=user).delete()
        attrs['user'] = user
        return attrs


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = "__all__"
