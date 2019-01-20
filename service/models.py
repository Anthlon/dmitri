from django.db import models


class ServiceTypeModel(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название категории услуг',
        db_index=True,
        unique=True
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        verbose_name='Порядковый номер'
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Содержание',
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'

    def __str__(self):
        return self.name


class ServiceModel(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название услуги',
    )
    content = models.TextField(
        verbose_name='Содержание',
    )
    service_type = models.ForeignKey(
        ServiceTypeModel,
        db_index=True,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория услуги'
    )







