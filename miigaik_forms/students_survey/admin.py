from django.contrib import admin

from .models import AnswerModel, StudentModel, SurveyStatusModel, TeacherCriteriaModel, QuestionsModel


# Register your models here.
@admin.register(AnswerModel)
class AnswerAdmin(admin.ModelAdmin):
    # list_display = ['answer']
    ...


@admin.register(QuestionsModel)
class QuestionsAdmin(admin.ModelAdmin):
    ...


@admin.register(TeacherCriteriaModel)
class TeacherCriteriaAdmin(admin.ModelAdmin):
    ...


@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['phone_number']


@admin.register(SurveyStatusModel)
class SurveyStatusAdmin(admin.ModelAdmin):
    list_display = ['is_active']
