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


TEMPLATES = {
    'index': 'students_survey/index.html',
    'result': 'students_survey/result.html'
}

URLS = {
    'result': '/survey/result'
}


# Create your views here.

class CheckStatusView(View):
    def get(self, r: WSGIRequest):
        if not SurveyStatusModel.objects.all()[0].is_active:
            return HttpResponse('Опрос недоступен!')

        return redirect(f'/survey/survey-q/')


class StudentLoginView(LoginView):
    template_name = TEMPLATES['index']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentDetailForm()
        return context


class AuthView(View):
    def get(self, request: WSGIRequest):
        form = StudentDetailForm()
        return render(request, template_name=TEMPLATES['index'], context={'form': form})

    def post(self, request: WSGIRequest):
        form = StudentDetailForm(request.POST)

        if not form.is_valid():
            return render(request, template_name=TEMPLATES['index'], context={'form': form})

        students = StudentModel.objects.filter(phone_number=form['phone_number'].value())

        if len(students):
            if students[0].has_survey:
                return HttpResponse('Вы уже прошли опрос')
        else:
            StudentModel.objects.create(phone_number=form['phone_number'].value(), start_survey=True)

        return redirect(f'/survey/check-status/')


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
            for question_id, ans in enumerate(AnswerModel().get_fields(), start=1):
                if question_id in [14, 15, 16, 17]: continue
                ans_text.append(questions.get_questions_ans(question_id, ans_id=row[ans])[0]['text'])
            ans_text.append(row['q14'])
            ans_text.append(row['q16'])

        context = {
            'students_len': len(students),
            'students': students,
            'answers_len': len(answers),
            'asks_text': asks_text,
            'ans_text': ans_text,
            'rows_len': [i for i in range(len(answers))],
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
