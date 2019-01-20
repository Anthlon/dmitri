from django.db import models
from personal_area.models import CustomUser


class DefenderModel(models.Model):
    class Meta:
        ordering = ['-last_parse']
        verbose_name = 'IP-адрес'
        verbose_name_plural = 'Ip-адреса'

    ip_address = models.GenericIPAddressField(
        verbose_name='ip адресс клиента',
        db_index=True,
        unique=True
    )
    total_counter = models.PositiveSmallIntegerField(
        verbose_name='Счетчик post-запросов',
        default=0
    )
    counter = models.PositiveSmallIntegerField(
        verbose_name='Счетчик post-запросов обнуляемый'
    )
    excess = models.BooleanField(
        default=True,
        verbose_name='Доступ разрешен или нет'
    )
    banned_dt = models.DateTimeField(
        verbose_name='Время до которого запрещен доступ',
        null=True,
        blank=True,
    )
    fist_parse = models.DateTimeField(
        auto_now_add=True
    )
    last_parse = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.ip_address


STATUS_CHOICES = (
    ('n', 'не указан'),
    ('p', 'по телефону'),
    ('e', 'по электронной почте'),
)


class FeedbackModel(models.Model):

    class Meta:
        ordering = ['-date_time_post']
        verbose_name = 'Запрос на обратную связь'
        verbose_name_plural = 'Запросы на обратную связь'

    name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    member = models.ForeignKey(
        DefenderModel,
        db_index=True,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ip клиента'
    )
    content = models.TextField(
        verbose_name='Содержание',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='email',
    )
    phone_number = models.CharField(  # ToDo: Номер телефона в форме
        max_length=17,
        null=True,
        blank=True,
        verbose_name='Номер телефона',
    )
    preferred = models.CharField(
        default='n',
        choices=STATUS_CHOICES,
        verbose_name='Предпочитаемый способ связи',
        max_length=1,
    )
    date_time_post = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время обращения'
    )

    def __str__(self):
        s = 'unknown'
        if self.name:
            s = '%s %s' % (self.name, self.date_time_post)
        return s





