import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Game


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = (
            "name",
            "duration",
            "status",
            "level"
        )
