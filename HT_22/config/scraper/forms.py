from django import forms

from . import utils


class SelectRubricForm(forms.Form):
    rubric = forms.ChoiceField(
        label="Выберите рубрику для cбора данных:", choices=utils.CHOICES)
