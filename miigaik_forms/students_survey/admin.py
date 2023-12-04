from django.contrib import admin

from .models import StudentModel, SurveyStatusModel, QuestionsModel


# Register your models here.


@admin.register(QuestionsModel)
class QuestionsAdmin(admin.ModelAdmin):
    ...


@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['cdo_login']


@admin.register(SurveyStatusModel)
class SurveyStatusAdmin(admin.ModelAdmin):
    list_display = ['is_active']
