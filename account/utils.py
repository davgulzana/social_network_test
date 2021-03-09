from django.conf import settings
from django.core.mail import send_mail


def send_activation_mail(user):
    subject = "Activating your account"
    host = settings.HOST_FOR_ACTIVATION
    body = (
        f"Thank you for registering on our website"
        f"To activate your account, follow the link:"
        f"{host}/api/v1/account/activate/{user.activation_code}/"
    )
    from_email = "test@gmail.com"
    recipients = [user.email]
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=recipients,
        fail_silently=False,
    )


def send_reset_password_mail(user):
    user.generate_password_reset_code()
    subject = "Password recovery."
    body = f"Password recovery code: {user.activation_code}"
    from_email = "test@gmail.com"
    recipients = [user.email]
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=recipients,
        fail_silently=False,
    )
