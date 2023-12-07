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
from .forms import StudentDetailForm, QuestionsForm
from .models import StudentModel, SurveyStatusModel, QuestionsModel
from .utils import Util

TEMPLATES = {
    'index': 'students_survey/index.html',
    'result': 'students_survey/result_distant.html',
    'questions': 'students_survey/questions.html',
    'distant_survey': 'students_survey/distant_survey.html',
    'survey': 'students_survey/survey.html'
}

URLS = {
    'result': '/survey/result/distant',
}

FILES_PATH = {
    'distant_res': 'media/result/результаты_дистант.xlsx'
}

FILES_URLS = {
    'distant_res': '/' + FILES_PATH['distant_res']
}

RESPONSE_MESSAGE = {
    'not_auth': '<h1>Авторизуйтесь!</h1>',
    'survey_success': '<h1>Опрос пройден</h1>',
    'survey_not_active': '<h1>Опрос не активен. Результаты не сохранены</h1>',
    'survey_done': '<h1>Вы уже прошли опрос ранее. Результаты не сохранены</h1>',
    'survey_active_for_delete_data': '<h1>Для удаления данных необходимо деактивировать опрос!</h1>'
}


class QuestionsView(View):
    def get(self, request: WSGIRequest):
        form = QuestionsForm()

        context = {
            'form': form
        }

        return render(request, TEMPLATES['questions'], context)

    def post(self, request: WSGIRequest):
        pass


# Create your views here.
class BookingWizardView(SessionWizardView):
    form_list = [StudentDetailForm, QuestionsForm]
    template_name = TEMPLATES['distant_survey']

    def done(self, form_list, **kwargs):

        if not SurveyStatusModel.objects.all()[0].is_active:
            return HttpResponse(RESPONSE_MESSAGE['survey_not_active'])

        students = StudentModel.objects.filter(cdo_login=form_list[0]['cdo_login'].value())

        if len(students):
            if students[0].has_survey:
                return HttpResponse(RESPONSE_MESSAGE['survey_not_active'])
            else:
                students[0].has_survey = True
                students[0].save()
        else:
            StudentModel.objects.create(cdo_login=form_list[0]['cdo_login'].value(), has_survey=True)

        QuestionsModel.objects.create(**form_list[1].cleaned_data)

        return HttpResponse(RESPONSE_MESSAGE['survey_success'])


class ResultView(View, LoginRequiredMixin):
    def get(self, r: WSGIRequest):

        if not self.request.user.is_authenticated:
            return HttpResponse(RESPONSE_MESSAGE['not_auth'])

        questions = Questions()

        students = StudentModel.objects.all()

        answers = list(QuestionsModel.objects.values())

        reformat_answers = Util.reformat_answers(answers)

        asks_text = Util.reformat_asks([el[1] for el in questions.get_questions_text()])

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
        if not self.request.user.is_authenticated:
            return HttpResponse(RESPONSE_MESSAGE['not_auth'])

        survey_status = SurveyStatusModel.objects.all()[0]

        answers = list(QuestionsModel.objects.values())

        questions = Questions()

        ans_headers = Util.reformat_asks([el[1] for el in questions.get_questions_text()])

        students_data = [[el.cdo_login, el.has_survey] for el in StudentModel.objects.all()]

        if 'deactivate_survey' in r.POST:
            survey_status.is_active = False

        elif 'activate_survey' in r.POST:
            survey_status.is_active = True

        elif 'delete_survey_data' in r.POST:
            if survey_status.is_active:
                return HttpResponse(RESPONSE_MESSAGE['survey_active_for_delete_data'])

            StudentModel.objects.all().delete()
            QuestionsModel.objects.all().delete()

        elif 'download_result' in r.POST:
            Util.generate_xlsx_file(FILES_PATH['distant_res'],
                                    students_data=Util.shuffle_the_list(students_data),
                                    students_headers=['Логин СДО', 'Прошел тест'],
                                    ans_data=Util.reformat_answers(Util.shuffle_the_list(answers)),
                                    ans_headers=ans_headers)

            return redirect(FILES_URLS['distant_res'])

        survey_status.save()

        return redirect(URLS['result'])


class SurveyView(TemplateView):
    template_name = TEMPLATES['survey']
