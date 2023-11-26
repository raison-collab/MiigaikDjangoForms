from django.contrib.auth.views import LoginView
from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from .forms import StudentDetailForm, AnswerDetailFormPart1, AnswerDetailFormPart2, AnswerDetailFormPart3
from .models import StudentModel, SurveyStatusModel, AnswerModel, TeacherCriteriaModel

status = True

TEMPLATES = {
    'index': 'students_survey/index.html'
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
    form_list = [AnswerDetailFormPart1, AnswerDetailFormPart2, AnswerDetailFormPart3]
    template_name = 'students_survey/survey.html'

    def done(self, form_list, **kwargs):

        student = StudentModel.objects.get()
        student.has_survey = True
        student.save()

        q15 = TeacherCriteriaModel.objects.create(**form_list[1].cleaned_data)
        q18 = TeacherCriteriaModel.objects.create(**form_list[2].cleaned_data)
        AnswerModel.objects.create(**form_list[0].cleaned_data, q15=q15, q18=q18)

        return HttpResponse('Опрос пройден!')


class ResultView(View):
    ...
