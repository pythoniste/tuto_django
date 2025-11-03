from django.test import TestCase, override_settings

from ..forms import BulkQuestionAnswerGenerationForm


class BulkQuestionAnswerGenerationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            "num_questions": 5,
            "question_prefix": "Q",
            "num_answers_per_question": 3,
            "answer_prefix": "R",
        }
        form = BulkQuestionAnswerGenerationForm(data=form_data)
        self.assertTrue(form.is_valid())

    @override_settings(LANGUAGE_CODE='fr-FR')
    def test_form_invalid_fr(self):
        form_data = {
            "num_questions": 500,
            "question_prefix": "Q" * 51,
            "num_answers_per_question": 0,
            "answer_prefix": "",
        }
        form = BulkQuestionAnswerGenerationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # print(dict(form.errors))
        self.assertEqual(
            form.errors,
            {
                'num_questions': ['Assurez-vous que cette valeur est inférieure ou égale à 100.'],
                'question_prefix': ['Assurez-vous que cette valeur comporte au plus 50 caractères (actuellement 51).'],
                'num_answers_per_question': ['Assurez-vous que cette valeur est supérieure ou égale à 1.'],
                'answer_prefix': ['Ce champ est obligatoire.'],
            },
        )

    @override_settings(LANGUAGE_CODE='en-US')
    def test_form_invalid_us(self):
        form_data = {
            "num_questions": 500,
            "question_prefix": "Q" * 51,
            "num_answers_per_question": 0,
            "answer_prefix": "",
        }
        form = BulkQuestionAnswerGenerationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # print(dict(form.errors))
        self.assertEqual(
            form.errors,
            {
                'num_questions': ['Ensure this value is less than or equal to 100.'],
                 'question_prefix': ['Ensure this value has at most 50 characters (it has 51).'],
                 'num_answers_per_question': ['Ensure this value is greater than or equal to 1.'],
                 'answer_prefix': ['This field is required.'],
            },
            # {
            #     'num_questions': ['Assurez-vous que cette valeur est inférieure ou égale à 100.'],
            #     'question_prefix': ['Assurez-vous que cette valeur comporte au plus 50 caractères (actuellement 51).'],
            #     'num_answers_per_question': ['Assurez-vous que cette valeur est supérieure ou égale à 1.'],
            #     'answer_prefix': ['Ce champ est obligatoire.'],
            # },
        )
