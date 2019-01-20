
from django.db import models


class AboutUsModel(models.Model):
    headline = models.TextField(
        verbose_name='Заголовок',
    )
    content = models.TextField(
        verbose_name='Содержание',
    )


class PreviousEmployment(models.Model):
    class Meta:
        ordering = ['-date_start']
        verbose_name = 'Предыдущее место работы'
        verbose_name_plural = 'Опыт работы'

    about = models.ForeignKey(AboutUsModel)

    organization = models.CharField(
        verbose_name='Организация',
        max_length=100,
    )
    date_start = models.DateField(
        db_index=True,
        verbose_name='Дата устройства на работу',
    )
    date_end = models.DateField(
        verbose_name='Дата ухода с работы',
    )
    post = models.CharField(
        verbose_name='Должность',
        max_length=100,
    )
    content = models.CharField(
        verbose_name='Содержание',
        max_length=5000
    )

    # def experience(self):
    #     delta = self.date_end - self.date_start
    #     years = delta.days//365
    #     month = (delta.days - years*365)//29
    #
    #     if years < 5:
    #         st = 'года'
    #         if years
    #     s = '%s, %s мес' % ()

    def __str__(self):
        s = 'unknown'
        if self.organization:
            s = '%s %s' % (self.organization, self.date_start)
        return s

