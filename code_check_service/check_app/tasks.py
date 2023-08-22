from __future__ import absolute_import

from celery.exceptions import MaxRetriesExceededError
from flake8.api import legacy as flake8
from flake8.formatting.default import Default
from django.core.mail import EmailMessage
import os

from check_app.models import File, Log
from code_check_service.celery import app
from code_check_service.settings import MEDIA_ROOT

#Задача на запуск проверки новых файлов
@app.task
def run_files_check():
    new_files = File.objects.filter(is_new=True)

    for file in new_files:
        path = os.path.join(MEDIA_ROOT, file.file.name)
        report = file_check(path)
        Log.objects.create(file=file, report=report)
        file.is_new = False
        file.save(update_fields=["is_new"])
    return True


class MyFormatter(Default):
    # Переопределяем один метод используемого форматтера flake8, чтобы исключить конфликт с логированием в celery
    def _write(self, output: str) -> None:
        if self.output_fd is not None:
            self.output_fd.write(output + self.newline)


def file_check(file_path):
    style_guide = flake8.get_style_guide()
    style_guide.init_report(reporter=MyFormatter)
    report = style_guide.input_file(file_path)
    result = report.get_statistics('E') + report.get_statistics('W')
    return ";\n".join(result) if len(result) else "quality code"

#Задача на отправку email с отчетом о проверке файла его автору
@app.task(default_retry_delay=45, max_retries=2)
def send_email_after_check(log_id, file_name, report, email_address):
    email = EmailMessage(
        'Отчет о проверке',
        f'Здравствуйте, ваш файл {file_name} проверен.\nРезультат:\n{report}',
        'settings.EMAIL_HOST_USER',
        [email_address]
    )
    try:
        email.send(fail_silently=False)
        Log.objects.filter(pk=log_id).update(is_send_notice=True)
    except Exception as e:
        print(e)
        try:
            send_email_after_check.retry()
        except MaxRetriesExceededError:
            print("Уведомление отправить не удалось")
    return True



