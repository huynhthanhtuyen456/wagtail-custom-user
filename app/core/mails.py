from django.core.mail import EmailMultiAlternatives


def send_confirm_code(to_email, message):
    mail = EmailMultiAlternatives(
        subject="Confirm code",
        from_email="noreply@goldenkey-software.com",
        to=[to_email, ],
        body=message
    )
    return mail.send()
