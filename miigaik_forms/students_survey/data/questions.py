import json
import os
import typing
from pprint import pprint


class Questions:
    def __init__(self):
        self.questions_path = 'students_survey/data/questions/questions.json'
        # self.questions_path = 'questions/questions.json'
        self.teacher_criteria_path = 'students_survey/data/questions/teacher_criteria.json'
        # self.teacher_criteria_path = 'questions/teacher_criteria.json'

    def get_questions(self, questions_id: typing.Optional[int] = None) -> list:
        with open(self.questions_path) as f:
            data = json.loads(f.read())

        if questions_id is not None:
            return [el for el in data if el['q_id'] == questions_id]

        return data

    def get_teacher_criteria(self, questions_id: typing.Optional[int] = None) -> list:
        with open(self.teacher_criteria_path) as f:
            data = json.loads(f.read())

        if questions_id is not None:
            return [el for el in data if el['q_id'] == questions_id]

        return data

    def get_questions_text(self, questions_id: typing.Optional[int] = None) -> list:
        if questions_id is not None:
            return [self.get_questions(questions_id)[0]['text']]
        return [(el['q_id'], el['text']) for el in self.get_questions()]

    def get_teacher_criteria_text(self, questions_id: typing.Optional[int] = None) -> list:
        if questions_id is not None:
            return [self.get_teacher_criteria(questions_id)[0]['text']]
        return [(el['q_id'], el['text']) for el in self.get_teacher_criteria()]

    def get_questions_ans(self, question_id: int, ans_id: typing.Optional[int] = None, choice: bool = False) -> list:
        current_question = self.get_questions(questions_id=question_id)[0]

        if ans_id is not None:
            if choice:
                return [[el['ans_id'], el['text']] for el in current_question['ans'] if el['ans_id'] == ans_id][0]
            return [el for el in current_question['ans'] if el['ans_id'] == ans_id]

        if choice:
            return [(ans['ans_id'], ans['text']) for ans in current_question['ans']]

        return current_question['ans']

    def get_teacher_criteria_ans(self, question_id: int, ans_id: typing.Optional[int] = None, choice: bool = False) -> list:
        current_question = self.get_teacher_criteria(questions_id=question_id)[0]

        if ans_id is not None:
            if choice:
                return [[el['ans_id'], el['text']] for el in current_question['ans'] if el['ans_id'] == ans_id][0]
            return [el for el in current_question['ans'] if el['ans_id'] == ans_id]

        if choice:
            return [(ans['ans_id'], ans['text']) for ans in current_question['ans']]

        return current_question['ans']
