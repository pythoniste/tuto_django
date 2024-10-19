import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as gettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Button
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import Game


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
