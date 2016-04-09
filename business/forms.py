from django import forms
from django.utils import timezone

from . import models


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        exclude = []
        widgets = {
            'name': forms.TextInput(),
            'email': forms.TextInput(),
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = ['project', 'note', 'number', 'date', 'unit_type']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = models.Project.active.select_related(
            'client').all()


class FilterForm(forms.Form):
    quarter = forms.ChoiceField(
        required=False,
        choices=reversed([(q, q) for q in models.get_quarters()]))
    project = forms.ModelChoiceField(
        required=False,
        queryset=models.Project.objects.all())


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = []
        widgets = {
            'name': forms.TextInput(),
            'start': forms.TextInput(attrs={'class': 'datepicker'}),
            'end': forms.TextInput(attrs={'class': 'datepicker'}),
        }


class RateForm(forms.ModelForm):
    class Meta:
        model = models.Rate
        exclude = []
        widgets = {
            'name': forms.TextInput(),
        }
