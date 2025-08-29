import roman
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

        modes = (
            Chant.objects.exclude(mode__isnull=True)
            .exclude(mode='')
            .values_list('mode', flat=True)
            .distinct()
            .order_by('mode')
        )
        self.fields['mode'].choices = [(m, self._mode_label(m)) for m in modes]

    def _mode_label(self, db_mode: str) -> str:
        if db_mode.isnumeric():
            return roman.toRoman(int(db_mode))

        return db_mode.upper()
