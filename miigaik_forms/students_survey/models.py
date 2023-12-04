from django.db import models

import re

from django.forms import RadioSelect

from .data.questions import Questions


# Create your models here.
class StudentModel(models.Model):
    cdo_login = models.CharField(max_length=15, verbose_name='Логин СДО')
    has_survey = models.BooleanField(default=False, verbose_name='Прошел опрос')

    def __str__(self):
        return str(self.cdo_login)


class QuestionsModel(models.Model):
    q1: models.IntegerField = models.IntegerField(verbose_name='')
    q1_dop: models.TextField = models.TextField(blank=True, null=True, default=None, verbose_name='Если да, то чему')
    q2: models.IntegerField = models.IntegerField(verbose_name='')
    q3: models.IntegerField = models.IntegerField(verbose_name='')
    q4: models.IntegerField = models.IntegerField(verbose_name='')
    q5: models.IntegerField = models.IntegerField(verbose_name='')
    q6: models.IntegerField = models.IntegerField(verbose_name='')
    q7: models.IntegerField = models.IntegerField(verbose_name='')
    q8: models.IntegerField = models.IntegerField(verbose_name='')
    q9: models.IntegerField = models.IntegerField(verbose_name='')
    q10: models.IntegerField = models.IntegerField(verbose_name='')
    q11: models.IntegerField = models.IntegerField(verbose_name='')
    q12: models.IntegerField = models.IntegerField(verbose_name='')
    q13: models.TextField = models.TextField(verbose_name='')
    q14: models.IntegerField = models.IntegerField(verbose_name='')
    q15: models.IntegerField = models.IntegerField(verbose_name='')
    q16: models.IntegerField = models.IntegerField(verbose_name='')
    q17: models.IntegerField = models.IntegerField(verbose_name='')
    q18: models.IntegerField = models.IntegerField(verbose_name='')
    q18_dop: models.TextField = models.TextField(blank=True, null=True, default=None, verbose_name='')

    def get_fields(self) -> list:
        return list(self.__annotations__.keys())


class SurveyStatusModel(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='Опрос активен')


