from pprint import pprint

from django.contrib.auth.views import LoginView
from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from .data.questions import Questions
from .forms import StudentDetailForm, AnswerDetailFormPart1, AnswerDetailFormPart2, AnswerDetailFormPart3
from .models import StudentModel, SurveyStatusModel, AnswerModel, TeacherCriteriaModel
from .utils import Util

TEMPLATES = {
    'index': 'students_survey/index.html',
    'result': 'students_survey/result.html'
}

URLS = {
    'result': '/survey/result'
}


# Create your views here.
class BookingWizardView(SessionWizardView):
    form_list = [StudentDetailForm, AnswerDetailFormPart1, AnswerDetailFormPart2, AnswerDetailFormPart3]
    template_name = 'students_survey/survey.html'

    def done(self, form_list, **kwargs):

        if not SurveyStatusModel.objects.all()[0].is_active:
            return HttpResponse('Ответы не сохранены. Форма неактивна')

        students = StudentModel.objects.filter(phone_number=form_list[0]['phone_number'].value())

        if len(students):
            if students[0].has_survey:
                return HttpResponse('Ответы не сохранены, Вы уже прошли опрос ранее!')
            else:
                students[0].has_survey = True
                students[0].save()
        else:
            StudentModel.objects.create(phone_number=form_list[0]['phone_number'].value(), has_survey=True)

        q15 = TeacherCriteriaModel.objects.create(**form_list[2].cleaned_data)
        q17 = TeacherCriteriaModel.objects.create(**form_list[3].cleaned_data)
        AnswerModel.objects.create(**form_list[1].cleaned_data, q15=q15, q17=q17)

        return HttpResponse('Опрос пройден!')


class ResultView(View):
    def get(self, r: WSGIRequest):

        questions = Questions()

        students = StudentModel.objects.all()

        answers = list(AnswerModel.objects.values())

        asks_text = [el[1] for el in questions.get_questions_text()]

        ans_text = []

        for row_index, row in enumerate(answers, start=1):
            row_info = []
            for question_id, ans in enumerate(AnswerModel().get_fields(), start=1):
                if question_id in [14, 15, 16, 17]: continue
                row_info.append(questions.get_questions_ans(question_id, ans_id=row[ans])[0]['text'])
            row_info.append(row['q14'])
            row_info.append(row['q16'])
            ans_text.append(row_info)

        context = {
            'students_len': len(students),
            'students': Util.shuffle_the_list(list(students)),
            'answers_len': len(answers),
            'asks_text': asks_text,
            'ans_text': Util.shuffle_the_list(ans_text),
            'is_active': SurveyStatusModel.objects.all()[0].is_active
        }

        return render(r, TEMPLATES['result'], context=context)

    def post(self, r: WSGIRequest):
        survey_status = SurveyStatusModel.objects.all()[0]
        if 'deactivate_survey' in r.POST:
            survey_status.is_active = False
        elif 'activate_survey' in r.POST:
            survey_status.is_active = True

        survey_status.save()

        return redirect(URLS['result'])
