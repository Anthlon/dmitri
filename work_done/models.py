from django.db import models
from taggit.managers import TaggableManager


class WorkDoneModel(models.Model):
    class Meta:
        ordering = ['-add_dt']
        verbose_name = 'Пример завершенной работы'
        verbose_name_plural = 'Примеры завершенных работ'

    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Полное содержание'
    )
    tags = TaggableManager(
        blank=True,
        verbose_name='Теги',
    )
    add_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )
    image = models.ImageField(
        upload_to='work_done/avatar',
        verbose_name='Основное изображение'
    )

    def save(self, *args, **kwargs):
        if self.pk:
            this_record = WorkDoneModel.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)


class WorkDoneImage(models.Model):
    work = models.ForeignKey(WorkDoneModel)
    image = models.ImageField(
        upload_to='work_done/detail',
        verbose_name='Дополнительное изображение'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        null=True,
        blank=True,
    )


