from datetime import timedelta

from django import forms
from django.forms import ModelChoiceField
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as gettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Row,
    Column,
    Div,
    Submit,
    Reset,
    Button,
    HTML,
    LayoutObject,
    TEMPLATE_PACK,
)
from crispy_forms.bootstrap import (
    FormActions,
    TabHolder,
    Tab,
    AppendedText,
    PrependedText,
    InlineRadios,
    AccordionGroup,
)
from crispy_bootstrap5.bootstrap5 import (
    FloatingField,
    BS5Accordion,
    Switch,
)
from martor.utils import markdownify

from .models import Game, Genre, Entry, Play, Question, Answer
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
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        if instance:
            buttons = (
                Submit('save', gettext('Update')),
            )
        else:
            buttons = (
                Submit('save', gettext('Create and add another')),
                Submit('save', gettext('Create and continue modification')),
                Submit('save', gettext('Create and go back to the list')),
            )
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    gettext("Main information"),
                    BS5Accordion(
                        AccordionGroup(
                            gettext("Name & genre"),
                            Row(
                                Column(
                                    Row(
                                        FloatingField("name"),
                                        css_class="",
                                    ),
                                    Row(
                                        PrependedText("genre", gettext("Game's genre")),
                                        css_class="",
                                    ),
                                    css_class="col-6",
                                ),
                                Column(
                                    Row(
                                        Div(
                                            Switch("highlight", gettext("Highlight")),
                                            css_class="col-6",
                                        ),
                                        Div(
                                            Switch("emphasize", gettext("Emphasize")),
                                            css_class="col-6",
                                        ),
                                    ),
                                    Row(
                                        Div(
                                            Switch("advertise", gettext("Advertise")),
                                            css_class="col-6",
                                        ),
                                        Div(
                                            Switch("recommend", gettext("Recommend")),
                                            css_class="col-6",
                                        ),
                                    ),
                                    Row("master"),
                                    css_class="col-6",
                                ),
                            ),
                            css_class="border p-4 mb-4 bg-success",
                        ),
                        AccordionGroup(
                            gettext("Description"),
                            "description",
                            css_class="border p-4 mb-4 bg-secondary"
                        ),
                        AccordionGroup(
                            gettext("About the game"),
                            Row(
                                Div(
                                    InlineRadios("level"),
                                    css_class="col-6",
                                ),
                                Div(
                                    "status",
                                    css_class="col-6",
                                ),
                            ),
                            css_class="border p-4 mb-4 bg-info"
                        ),
                    ),
                    flush=True,
                    # always_open=True
                ),
                Tab(
                    gettext("Duration"),
                    Fieldset(
                        gettext("Duration"),
                        Row(
                            Div(
                                AppendedText("duration_day", gettext("days")),
                                css_class="col-6",
                            ),
                            Div(
                                AppendedText("duration_hour", gettext("hours")),
                                css_class="col-6",
                            ),
                            Div(
                                AppendedText("duration_minute", gettext("minutes")),
                                css_class="col-6",
                            ),
                            Div(
                                AppendedText("duration_second", gettext("seconds")),
                                css_class="col-6",
                            ),
                        ),
                        css_class="border p-4 mb-4 bg-light"
                    ),
                ),
            ),
            FormActions(
                *buttons,
                Reset('cancel', gettext('Reset'), css_class="btn-danger"),
            ),
        )


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
            "highlight",
            "emphasize",
            "master",
            "advertise",
            "recommend",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'bulk_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = True  # This is the default value
        self.helper.disable_csrf = False  # This is the default value
        self.helper.render_unmentioned_fields = False  # This is the default value
        self.helper.render_hidden_fields = False  # This is the default value
        self.helper.render_required_fields = False  # This is the default value
        self.helper.layout = Layout(
            Fieldset(
                gettext("Please fill out the form"),
                Row(
                    Div(
                        FloatingField("num_questions"),
                        css_class="col-6",
                    ),
                    Div(
                        FloatingField("question_prefix"),
                        css_class="col-6",
                    ),
                ),
                Row(
                    Div(
                        FloatingField("num_answers_per_question"),
                        css_class="col-6",
                    ),
                    Div(
                        FloatingField("answer_prefix"),
                        css_class="col-6",
                    ),
                ),
                css_class="border p-4 mb-4 bg-dark"
            ),
            FormActions(
                Submit('save', gettext('Bulk create questions and responses')),
                Reset('reset', gettext('Reset'), css_class="btn-danger"),
                Button('default', gettext('Set default values'), css_class="btn-info", onclick="setDefaultValues()"),
            ),
        )


class EntryForm(forms.ModelForm):

    answer = ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=Answer.objects.none()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["answer"].queryset = self.instance.question.answer_set.all()
        self.fields["answer"].label = self.instance.question.text

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML(
                        self.instance.question.text
                    )
                ),
                Row(
                    Field("answer", css_class='input-xlarge', style="background: #FAFAFA; padding: 10px;"),
                ),
                FormActions(
                    Submit('save', gettext('Validate answers')),
                    Button('cancel', gettext('Cancel'), css_class="btn-danger"),
                ),
                css_class="container",
            ),
        )

    class Meta:
        model = Entry
        fields = (
            "play",
            "answer",
        )
        widgets = {
            "play": forms.HiddenInput(),
        }


PlayFormSet = inlineformset_factory(
    Play,
    Entry,
    form=EntryForm,
    fields=["play", 'answer'],
    extra=0,
    can_delete=False,
    edit_only=True,
)


class PlayFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(
                Row(
                    Field("answer", css_class='input-xlarge', style="background: #FAFAFA; padding: 10px;"),
                ),
                css_class="container",
            ),
        )


class QuestionLayout(LayoutObject):
    template = "app/play_formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        helper = PlayFormSetHelper()
        return render_to_string(self.template, {'formset': formset, "helper": helper})


class PlayForm(forms.ModelForm):

    entry_set = PlayFormSet()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Row(
                    HTML(
                        gettext("<h5>You are playing the game <strong>{}</strong></h5>").format(
                            self.instance.game.name
                        )
                    ),
                ),
                Row(
                    HTML(markdownify(self.instance.game.description)),
                ),
                Row(
                    QuestionLayout('entry_set'),
                ),
                FormActions(
                    Submit('save', gettext('Validate answers')),
                    Button('cancel', gettext('Cancel'), css_class="btn-danger"),
                ),
                css_class="container",
            )
        )

    class Meta:
        model = Play
        fields = ()
