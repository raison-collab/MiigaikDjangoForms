from django.urls import path

from . import views

urlpatterns = [
    # path('check-status/', views.CheckStatusView.as_view(), name='check_status_page'),
    path('survey-q/', views.BookingWizardView.as_view(), name='survey_questions_page'),
    path('', views.AuthView.as_view(), name='auth_page'),
    path('result/', views.ResultView.as_view(), name='result_survey_page')
]
