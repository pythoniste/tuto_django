from django.forms import ModelChoiceField

from .models import Category


class CategoryChoiceField(ModelChoiceField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pk_order = [c.pk for c in Category.objects.tree()]
        pk_index = {pk: index for index, pk in enumerate(pk_order, start=1)} | {'': 0}
        self.choices = sorted(self.choices, key=lambda x: pk_index[x[0]])

    def label_from_instance(self, obj):
        return obj.deep_label
