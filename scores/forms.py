from django import forms

from .models import Chant


class ChantFilterForm(forms.Form):
    incipit = forms.CharField(required=False, label='Incipit')
    office_part = forms.MultipleChoiceField(
        required=False,
        label='Usage',
        widget=forms.CheckboxSelectMultiple
    )
    mode = forms.MultipleChoiceField(
        required=False,
        label='Mode',
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Flatten grouped OFFICE_PART_CHOICES into simple (code, label) list
        office_choices = []
        for _group_name, items in Chant.OFFICE_PART_CHOICES:
            for code, label in items:
                office_choices.append((code, label))
        self.fields['office_part'].choices = office_choices

        self.fields['mode'].choices = Chant.MODE_CHOICES
