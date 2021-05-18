from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token

from core.utils import get_absolute_url_adapter


class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, uidb64, token, **kwargs):
        return f"{settings.BASE_URL.rstrip('/')}/v1/auth/activate/{uidb64}/{token}/"

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(
            request,
            uidb64=urlsafe_base64_encode(force_bytes(emailconfirmation.email_address.user.pk)),
            token=account_activation_token.make_token(emailconfirmation.email_address.user)
        )
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site.domain,
            "key": emailconfirmation.key,
            "logo_url": get_absolute_url_adapter(request, 'logo-white.png'),
            "expire_day": settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
            "frontend_url": settings.FRONTEND_BASE_URL
        }
        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)
