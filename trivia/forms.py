from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

class TriviaForm(forms.Form):
    question_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

class TextTriviaForm(TriviaForm):
    answer = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class CheckTriviaForm(TriviaForm):
    answer = forms.MultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'answers'})
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].choices = choices

class RadioTriviaForm(TriviaForm):
    answer = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect(attrs={'class': 'answers'})
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].choices = choices