from django.db import models


class User(models.Model):
    COMPANY = (
        ('kraseco', 'КрасЭко'),
        ('kic', 'КИЦ'),
        ('ministry', 'Министерство'),
    )

    DEPARTMENT = (
        ('general', 'Общий'),
    )

    last_name = models.CharField('ФИО', max_length=40)
    number = models.CharField('Номер', max_length=5, unique=True)
    mobile = models.CharField('Мобильный', max_length=11, blank=True)
    mac_adress = models.CharField('MAC-адрес', max_length=12, blank=True)
    panel = models.BooleanField('Панель расширения', default=False)
    company = models.CharField('Компания', max_length=20, default=COMPANY[0][0], choices=COMPANY)
    department = models.CharField('Отдел', max_length=20, default=DEPARTMENT[0][0], choices=DEPARTMENT)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.last_name


class ExtendedNumber(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'panel': True}, verbose_name='Просматривает')
    key = models.PositiveSmallIntegerField('Кнопка')
    name = models.CharField('Имя', max_length=20)
    number = models.CharField('Номер', max_length=11)
    module = models.PositiveSmallIntegerField('Модуль', default=1)

    class Meta:
        verbose_name = "Номер на панели"
        verbose_name_plural = "Номера на панели"

    def __str__(self):
        return " ".join([self.name, self.number])