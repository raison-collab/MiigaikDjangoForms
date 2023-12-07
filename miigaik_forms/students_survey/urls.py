from django.urls import path

from . import views

urlpatterns = [
    path('survey-q/distant/', views.BookingWizardView.as_view(), name='survey_questions_page'),
    path('result/distant/', views.ResultView.as_view(), name='result_distant_survey_page'),
    path('', views.SurveyView.as_view(), name='survey_view_page')
]
