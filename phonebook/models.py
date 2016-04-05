from django.db import models


class User(models.Model):
    last_name = models.CharField("Фамилия", max_length=20, blank=True)
    second_name = models.CharField("Фамилия", max_length=20, blank=True)
    name = models.CharField("Имя", max_length=20, blank=True)
    number = models.CharField("Телефон", max_length=5, unique=True)
    mobile = models.CharField("Мобильный", max_length=10, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return " ".join([self.last_name, self.name, self.second_name])