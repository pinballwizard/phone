from django.db import models


class User(models.Model):
    COMPANY = (
        ('kraseco', 'Красэко'),
        ('kic', 'КИЦ'),
        ('ministry', 'Министерство'),
    )
    DEPARTMENTS = (
        ('Красэко', (
            ('general', 'Общий'),
            ('administrator', 'Адиминистративная служба'),
            ('accounting', 'Бухгалтерия'),
            ('director', 'Дирекция'),
            ('engineer', 'Служба главного инженера'),
            ('secretory', 'Служба делопроизводства'),
            ('build', 'Служба капитального строительства'),
            ('law', 'Служба по правовым вопросам'),
            ('sell', 'Служба реализации услуг'),
            ('supply', 'Служба снабжения'),
            ('control', 'Служба финансового контроля'),
            ('finance', 'Финансово-экономическая служба'),
            )
        ),
        ('КИЦ', (
            ('kic_general', 'Общий'),
            )
        ),
        ('Министерство', (
            ('min_general', 'Общий'),
            )
        ),
    )

    last_name = models.CharField('ФИО', max_length=40)
    name = models.CharField('Имя', max_length=40, default=None, blank=True)
    second_name = models.CharField('Отчество', max_length=40, default=None, blank=True)
    number = models.CharField('Номер', max_length=5, unique=True)
    mobile = models.CharField('Мобильный', max_length=11, blank=True)
    mac_adress = models.CharField('MAC-адрес', max_length=12, blank=True)
    panel = models.BooleanField('Панель расширения', default=False)
    voice_mail = models.BooleanField('Голосовая почта', default=False)
    company = models.CharField('Компания', max_length=50, default=COMPANY[0][0], choices=COMPANY)
    department = models.CharField('Отдел', max_length=50, default='general', choices=DEPARTMENTS)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.last_name
        # return '{0} {1}.{2}.'.format(self.last_name, self.name[0], self.second_name[0])


class SideNumber(models.Model):
    name = models.CharField('Имя', max_length=20)
    number = models.CharField('Номер', max_length=11)

    class Meta:
        verbose_name = "Сторонний номер"
        verbose_name_plural = "Сторонние номера"

    def __str__(self):
        return " ".join([self.name, self.number])


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