from django.forms.widgets import RadioSelect
from django.utils.translation import gettext_lazy as gettext


class NullBooleanRadioSelect(RadioSelect):
    template_name = 'django/forms/widgets/horizontal_radio.html'

    def __init__(self, *args, **kwargs):
        choices = (
            (None, gettext('Unknown')),
            (True, gettext('Yes')),
            (False, gettext('No'))
        )
        super().__init__(choices=choices, *args, **kwargs)

    _empty_value = None
