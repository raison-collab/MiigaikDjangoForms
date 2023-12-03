from django.urls import path

from . import views

urlpatterns = [
    path('survey-q/', views.BookingWizardView.as_view(), name='survey_questions_page'),
    path('survey-q1/', views.QuestionsView.as_view(), name='survey_questions_page1'),
    path('result/', views.ResultView.as_view(), name='result_survey_page')
]
