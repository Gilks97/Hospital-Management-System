from django.core.mail import send_mail
from django.conf import settings


def send_forgot_password_mail(user_obj, token):
    subject = 'Reset Your Password'
    message = f'Hi  ,\n\nPlease click the following link to reset your password:\n\n  http://127.0.0.1:8000/change-pass/{token}\n\nIf you did not request a password reset, please ignore this email.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_obj.email]
    send_mail(subject, message, from_email, recipient_list)
    return True
