from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Log
from check_app.tasks import send_email_after_check


@receiver(post_save, sender=Log)
def post_create_update_order(created, instance, **kwargs):
    if created:
        file_name = instance.file.file.name.split('/')[-1]
        # После создания лога проверки вызываем задачу на отправку email с отчетом автору соответствующего файла
        send_email_after_check.delay(instance.id, file_name, instance.report, instance.file.user.email)
