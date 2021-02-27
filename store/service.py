from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


def send(user_email):
    send_mail(
        _('Вы подписались на рассылку'),
        _('Мы будем присылать вам информацию об акциях и новинках.'),
        'eskermesernur86@gmail.com',
        [user_email],
        fail_silently=False,
    )
