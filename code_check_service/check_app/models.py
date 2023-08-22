import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('Email адрес', max_length = 254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


def get_path_upload_file(file, user):
    extention = file.split('.')[1]
    head = file.split('.')[0]
    if len(head) > 25:
        head = head[:25]
    file_name = head + '.' + extention
    return os.path.join('{}', '{}').format(user, file_name)


class File(models.Model):
    file = models.FileField("Файл", upload_to="files/", validators=[FileExtensionValidator(['py'])])
    user = models.ForeignKey(User, db_column="user_id", verbose_name="Автор", related_name="files", on_delete=models.CASCADE)
    description = models.TextField("Описание", blank=True, null=True)
    is_new = models.BooleanField("Новый файл", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    def __str__(self):
        return "{}".format(self.file.name)

    def save(self, *args, **kwargs):
        if not self.file.name.startswith("files/"):
            self.file.name = get_path_upload_file(self.file.name, self.user)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ('-updated_at',)


class Log(models.Model):
    file = models.ForeignKey(File, verbose_name="Файл", related_name='logs', on_delete=models.CASCADE)
    report = models.TextField("Результат проверки", max_length=5000, null=False)
    date = models.DateTimeField("Дата проверки", auto_now_add=True)
    is_send_notice = models.BooleanField("Сообщение отправлено", default=False)

    def __str__(self):
        return "{}_{}".format(self.file, self.date)

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
        ordering = ('-date',)