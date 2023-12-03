from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sessions.backends.db import SessionStore
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView

from .data.questions import Questions
from .forms import StudentDetailForm, AnswerDetailFormPart1, AnswerDetailFormPart2, AnswerDetailFormPart3, QuestionsForm
from .models import StudentModel, SurveyStatusModel, AnswerModel, TeacherCriteriaModel, QuestionsModel
from .utils import Util

TEMPLATES = {
    'index': 'students_survey/index.html',
    'result': 'students_survey/result.html',
    'questions': 'students_survey/questions.html'
}

URLS = {
    'result': '/survey/result',
    'login': '/auth/login/'
}


class QuestionsView(View):
    def get(self, request: WSGIRequest):
        form = QuestionsForm()

        fields = QuestionsModel().get_fields()
        pprint([fields[0]] + fields[2: 13] + fields[13: 19])

        context = {
            'form': form
        }

        return render(request, TEMPLATES['questions'], context)

    def post(self, request: WSGIRequest):
        pass


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


class ResultView(View, LoginRequiredMixin):
    def get(self, r: WSGIRequest):

        questions = Questions()

        students = StudentModel.objects.all()

        answers = list(AnswerModel.objects.values())

        reformat_answers = Util.reformat_answers(answers)

        asks_text = [el[1] for el in questions.get_questions_text()]

        context = {
            'students_len': len(students),
            'students': Util.shuffle_the_list(list(students)),
            'answers_len': len(answers),
            'asks_text': asks_text,
            'ans_text': Util.shuffle_the_list(reformat_answers),
            'is_active': SurveyStatusModel.objects.all()[0].is_active
        }

        return render(r, TEMPLATES['result'], context=context)

    def post(self, r: WSGIRequest):
        # todo Доделать авторизацию
        # if not self.request.user.is_authenticated:
        #     return redirect(URLS['login'])

        survey_status = SurveyStatusModel.objects.all()[0]

        answers = list(AnswerModel.objects.values())

        questions = Questions()

        ans_headers = [el[1] for el in questions.get_questions_text()]

        students_data = [[el.phone_number, el.has_survey] for el in StudentModel.objects.all()]

        if 'deactivate_survey' in r.POST:
            survey_status.is_active = False

        elif 'activate_survey' in r.POST:
            survey_status.is_active = True

        elif 'delete_survey_data' in r.POST:
            if survey_status.is_active:
                return HttpResponse('<h1>Для удаления данных необходимо деактивировать опрос</h1>')
            print('удаление данных....')
            # todo Удаление данных

        elif 'download_result' in r.POST:
            Util.generate_xlsx_file('result/результаты.xlsx',
                                    students_data=Util.shuffle_the_list(students_data),
                                    students_headers=['Номер тел.', 'Прошел тест'],
                                    ans_data=Util.reformat_answers(Util.shuffle_the_list(answers)),
                                    ans_headers=ans_headers)

        survey_status.save()

        return redirect(URLS['result'])
