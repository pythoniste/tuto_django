from datetime import timedelta

from django import forms
from django.utils.translation import gettext_lazy as gettext

from .models import Game, Genre
from .fields import TreeChoiceField


class GameForm(forms.ModelForm):
    duration_day = forms.IntegerField(
        label=gettext("Day"),
        min_value=0,
        max_value=23,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": gettext("Day"), "min": "0"})
    )

    duration_hour = forms.IntegerField(
        label=gettext("Hour"),
        min_value=0,
        max_value=23,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": gettext("Hour"), "min": "0", "max": "23"})
    )

    duration_minute = forms.IntegerField(
        label=gettext("Minute"),
        min_value=0,
        max_value=59,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": gettext("Minute"), "min": "0", "max": "59"})
    )

    duration_second = forms.IntegerField(
        label=gettext("Second"),
        min_value=0,
        max_value=59,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": gettext("Second"), "min": "0", "max": "59"})
    )

    genre = TreeChoiceField(
        queryset=Genre.objects.all(),
        label=gettext("Genre"),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance:
            duration = instance.duration

            if duration:
                total_seconds = int(duration.total_seconds())
                jour = total_seconds // 86400
                total_seconds %= 86400
                hour = total_seconds // 3600
                total_seconds %= 3600
                minute = total_seconds // 60
                second = total_seconds % 60

                # Set the initial values for the form fields
                kwargs["initial"] = kwargs.get("initial", {}) | {
                    "duration_day": jour,
                    "duration_hour": hour,
                    "duration_minute": minute,
                    "duration_second": second,
                }
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        day = cleaned_data.pop("duration_day", 0)
        hour = cleaned_data.pop("duration_hour", 0)
        minute = cleaned_data.pop("duration_minute", 0)
        second = cleaned_data.pop("duration_second", 0)

        cleaned_data["duration"] = timedelta(seconds=(day * 86400) + (hour * 3600) + (minute * 60) + second)

    class Meta:
        model = Game
        fields = (
            "name",
            "description",
            "duration",
            "duration_day",
            "duration_hour",
            "duration_minute",
            "duration_second",
            "status",
            "level",
            "genre",
        )
        widgets = {
            "duration": forms.HiddenInput(),
            "level": forms.RadioSelect(),
        }


class BulkQuestionAnswerGenerationForm(forms.Form):

    num_questions = forms.IntegerField(
        label=gettext("Number of questions"),
        min_value=1,
        max_value=100,
    )

    question_prefix = forms.CharField(
        label=gettext("Question prefix"),
        max_length=50,
    )

    num_answers_per_question = forms.IntegerField(
        label=gettext("Number of anwser per question"),
        min_value=1,
        max_value=10,
    )

    answer_prefix = forms.CharField(
        label=gettext("Answer prefix"),
        max_length=50,
    )


