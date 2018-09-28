from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article, Subscribe


@receiver(post_save, sender=Article)
def send_subscribe_emails(sender, instance, created, **kwargs):
    if created:
        mail_data = {
            'subject': 'Новая запись в блоге',
            'from_email': 'admin@testblog.ru',
            'message': 'ссылка: http://localhost.local/{}'.format(instance.get_absolute_url())
        }
        followers = Subscribe.objects.prefetch_related('follower')\
            .filter(target_id=instance.author_id)\
            .values_list('follower__email', flat=True)
        send_mail(recipient_list=[followers], **mail_data)
