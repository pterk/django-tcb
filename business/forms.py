from django import forms

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
