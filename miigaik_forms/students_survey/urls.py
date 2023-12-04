from django.urls import path

from . import views

urlpatterns = [
    path('survey-q/distant/', views.BookingWizardView.as_view(), name='survey_questions_page'),
    path('result/distant/', views.ResultView.as_view(), name='result_survey_page'),
    path('download/distant/', views.download_file, name='download_distant_page')
]
