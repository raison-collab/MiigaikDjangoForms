from django import forms

from .data.questions import Questions
from .models import StudentModel, QuestionsModel

questions = Questions()


def generate_widget_for_radio_btns(fields: list[str]) -> dict:
    widgets = {}

    for field in fields:
        widgets[field] = forms.RadioSelect(choices=questions.get_questions_ans(int(field.replace('q', '')), choice=True),
                                                attrs={
                                                    'type': 'radio',
                                                })

    return widgets


def generate_label_for_radio_btns(fields: list[str]) -> dict:
    labels = {}

    for field in fields:
        labels[f'{field}'] = questions.get_questions_text(int(field.replace('q', '')))[0]

    return labels


class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = ('cdo_login',)
        widgets = {
            'cdo_login': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш логин СДО'
            })
        }


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = QuestionsModel
        fields = QuestionsModel().get_fields()
        widgets = generate_widget_for_radio_btns([fields[0]] + fields[2: 13] + fields[14: 19]) | {
            'q1_dop': forms.TextInput(attrs={'class': 'form-control'}),
            'q18_dop': forms.TextInput(attrs={'class': 'form-control'}),
            'q13': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = generate_label_for_radio_btns([fields[0]] + fields[2: 19]) | {
            'q18_dop': 'Какие конкретно'
        }
