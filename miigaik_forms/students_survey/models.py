from django.db import models

import re

from django.forms import RadioSelect

from .data.questions import Questions


# Create your models here.
class StudentModel(models.Model):
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    has_survey = models.BooleanField(default=False, verbose_name='Прошел опрос')
    # start_survey = models.BooleanField(default=False, verbose_name='Начал тест')

    def __str__(self):
        phone = self.phone_number
        # f'{phone[:2]}({phone[2:5]}){phone[5:8]}-{phone[8:10]}-{phone[10:12]}'
        return self.phone_number


class TeacherCriteriaModel(models.Model):
    q1: models.IntegerField = models.IntegerField(verbose_name='Информат-ные л-ции без "воды"')
    q2: models.IntegerField = models.IntegerField(verbose_name='Свободно отвечает на вопросы студ-ов')
    q3: models.IntegerField = models.IntegerField(verbose_name='Объясняет знач предмета для буд проф-ий')
    q4: models.IntegerField = models.IntegerField(verbose_name='Приводит приеры реальной из реал-ой прак-ки ')
    q5: models.IntegerField = models.IntegerField(verbose_name='Умеет орг-ть дискуссию по теме')
    q6: models.IntegerField = models.IntegerField(verbose_name='Излагает материал в доступной форме')
    q7: models.IntegerField = models.IntegerField(verbose_name='Зад/вопр в с/р сложнее чем матер-ал рассм-мый в аудитории')
    q8: models.IntegerField = models.IntegerField(verbose_name='Отмеч присут-ие студ-ов')
    q9: models.IntegerField = models.IntegerField(verbose_name='Соблюдает уч расп-ие')
    q10: models.IntegerField = models.IntegerField(verbose_name='Повыш голос, прояв-ет неуваж к студ-там')
    q11: models.IntegerField = models.IntegerField(verbose_name='Учитывает жиз-ые обст-ва студ-ов')
    q12: models.IntegerField = models.IntegerField(verbose_name='Заинтересовывает излаг-ым мат-лом')
    q13: models.IntegerField = models.IntegerField(verbose_name='Обознач свою сист треб-ний и четко собл-ет ее')
    q14: models.IntegerField = models.IntegerField(verbose_name='Рекомендую курс данного преп-ля')

    def get_fields(self) -> list:
        return list(self.__annotations__.keys())


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


class AnswerModel(models.Model):
    q1: models.IntegerField = models.IntegerField(verbose_name='Пол')
    q2: models.IntegerField = models.IntegerField(verbose_name='Факультет')
    q3: models.IntegerField = models.IntegerField(verbose_name='Форма обучения')
    q4: models.IntegerField = models.IntegerField(verbose_name='Курс')
    q5: models.IntegerField = models.IntegerField(verbose_name='Нравится ли обучение в МИИГАиК')
    q6: models.IntegerField = models.IntegerField(verbose_name='В основном ты учишься')
    q7: models.IntegerField = models.IntegerField(verbose_name='Как часто ты готовишься к занятиям')
    q8: models.IntegerField = models.IntegerField(verbose_name='Насколько важн ароль преподавателя')
    q9: models.IntegerField = models.IntegerField(verbose_name='Стиль препод-я у твоих род-ей в большей ст-ни схож с')
    q10: models.IntegerField = models.IntegerField(verbose_name='Лучшие препод-ли в возр-те')
    q11: models.IntegerField = models.IntegerField(verbose_name='Должен ли преп-ль иметь опыт раб. по спец-ти, помимо педад-кой д-ти')
    q12: models.IntegerField = models.IntegerField(verbose_name='Какие  кач-ва в преп-ле ты цених больше всего')
    q13: models.IntegerField = models.IntegerField(verbose_name='Есть ли "идеяльный" преп-ль')
    q14: models.CharField = models.CharField(max_length=200, verbose_name='Лучший преп-ль')
    q15: models.ForeignKey = models.ForeignKey('TeacherCriteriaModel', on_delete=models.SET_NULL, null=True, related_name='survey_questions_best', verbose_name='кач-ва преп-ля')
    q16: models.CharField = models.CharField(max_length=200, verbose_name='Есть ли "худший" преп-ль')
    q17: models.ForeignKey = models.ForeignKey('TeacherCriteriaModel', on_delete=models.SET_NULL, null=True, related_name='survey_questions_worth', verbose_name='кач-ва преп-ля')

    # def __str__(self):
    #     return f'{self.answer:25}'

    def get_fields(self) -> list:
        return list(self.__annotations__.keys())


class SurveyStatusModel(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='Опрос активен')


