from django.forms import ModelChoiceField


class TreeChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.deep_label
