import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gettext
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Button, LayoutObject, TEMPLATE_PACK
from crispy_forms.bootstrap import FormActions, AppendedText, Div, Field
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Game, Entry, Play, Question


class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                gettext("main data"),
                FloatingField("name"),
                AppendedText("duration", "secondes"),
                Row(
                    "level",
                    "status",
                ),
            ),
            FormActions(
                Submit('save', gettext('Update')),
                Button('cancel', gettext('Cancel'), css_class="btn-danger"),
            ),
        )

    class Meta:
        model = Game
        fields = (
            "name",
            "duration",
            "status",
            "level"
        )


class EntryForm(forms.ModelForm):

    question_id = forms.CharField(widget=forms.HiddenInput())

    question_text = forms.CharField(
        widget=forms.Textarea(),
        disabled=True,
    )

    answer = forms.ChoiceField(
        widget=forms.RadioSelect,
    )

    def get_initial_for_field(self, field, field_name):
        result = super().get_initial_for_field(field, field_name)
        if field_name == "question_id":
            return self.instance.question_id
        if field_name == "question_text":
            return Question.objects.get(pk=self.instance.question_id).text
        if field_name == "answer":
            question = Question.objects.get(pk=self.instance.question_id)
            field.choices = [
                (answer.pk, answer.text) for answer in question.answer_set.all()
            ]
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        # self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            "question_id",
            Field("question_text", rows="3", css_class='input-xlarge'),
            Field("answer",  css_class='input-xlarge', style="background: #FAFAFA; padding: 10px;"),
        )

    # def is_valid(self) -> bool:
    #     # super().is_valid
    #     return True
    #
    # def save(self, *args, **kwargs):
    #     Entry.objects.filter(pk=self.instance.pk).update(answer=self.answer.value)
    #     # self.instance.save(update_fields=["answer"])

    class Meta:
        model = Entry
        fields = (
            "question_id",
            "answer",
        )
        # widgets = {
        #     'question_id': forms.ChoiceField(required=True, disabled=True)
        # }


PlayFormSet = inlineformset_factory(
    Play,
    Entry,
    form=EntryForm,
    fields=['question_id', 'answer'],
    extra=0,
    can_delete=False,
)


class PlayFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            "question_id",
            Field("question_text", rows="3", css_class='input-xlarge'),
            Field("answer",  css_class='input-xlarge', style="background: #FAFAFA; padding: 10px;"),
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
        return render_to_string(self.template, {'formset': formset})


class PlayForm(forms.ModelForm):

    game_id = forms.CharField(widget=forms.HiddenInput())

    game_name = forms.CharField(
        disabled=True,
    )

    entry_set = PlayFormSet()

    def get_initial_for_field(self, field, field_name):
        result = super().get_initial_for_field(field, field_name)
        if field_name == "game_id":
            return self.instance.game.pk
        if field_name == "game_name":
            return self.instance.game.name
        return result

    # def is_valid(self) -> bool:
    #     return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                "game_id",
                Field('game_name'),
                Fieldset('Questions', QuestionLayout('entry_set')),
                FormActions(
                    Submit('save', gettext('Update')),
                    Button('cancel', gettext('Cancel'), css_class="btn-danger"),
                ),
            )
        )

    class Meta:
        model = Play
        fields = (
            "game_id",
        )
