import random
import string

from django.core.mail import send_mail

CONFIRMATION_CODE_LEN = 10


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Код подтверждения для регистрации',
        message='Благодарим за регистрацию на Yamdb. '
                f'Код подтверждения: {confirmation_code}',
        from_email='support@yambd.ru',
        recipient_list=[email],
        fail_silently=False,
    )


def generate_confirmation_code():
    return ''.join(random.choices(string.digits + string.ascii_uppercase,
                                  k=CONFIRMATION_CODE_LEN))
