from django import forms

from .data.questions import Questions
from .models import StudentModel, AnswerModel, TeacherCriteriaModel

questions = Questions()


def generate_widget_for_radio_btns(fields: list[str], is_tacher: bool = False) -> dict:
    widgets = {}

    if is_tacher:
        for field in fields:
            widgets[f'{field}'] = forms.RadioSelect(
                choices=questions.get_teacher_criteria_ans(int(field.replace('q', '')), choice=True),
                attrs={'type': 'radio'})

        return widgets

    for field in fields:
        widgets[f'{field}'] = forms.RadioSelect(choices=questions.get_questions_ans(int(field.replace('q', '')), choice=True),
                                                attrs={'type': 'radio'})

    return widgets


def generate_label_for_radio_btns(fields: list[str], is_teacher: bool = False) -> dict:
    labels = {}

    if is_teacher:
        for field in fields:
            labels[f'{field}'] = questions.get_teacher_criteria_text(int(field.replace('q', '')))[0]
        return labels

    for field in fields:
        labels[f'{field}'] = questions.get_questions_text(int(field.replace('q', '')))[0]

    return labels


class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = ('phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7XXXXXXXXXX'
            })
        }


class AnswerDetailFormPart1(forms.ModelForm):

    class Meta:
        model = AnswerModel
        fields = list(AnswerModel().get_fields())[:14] + [AnswerModel().get_fields()[15]]
        widgets = generate_widget_for_radio_btns(fields[:-2]) | {
            'q14': forms.TextInput(attrs={'class': 'form-control'}),
            'q17': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = generate_label_for_radio_btns(fields)


class AnswerDetailFormPart2(forms.ModelForm):
    class Meta:
        model = TeacherCriteriaModel
        fields = TeacherCriteriaModel().get_fields()
        widgets = generate_widget_for_radio_btns(fields, is_tacher=True)
        labels = generate_label_for_radio_btns(fields, is_teacher=True)


class AnswerDetailFormPart3(AnswerDetailFormPart2):

    class Meta:
        model = TeacherCriteriaModel
        fields = TeacherCriteriaModel().get_fields()
        widgets = generate_widget_for_radio_btns(fields, is_tacher=True)
        labels = generate_label_for_radio_btns(fields, is_teacher=True)
