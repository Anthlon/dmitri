

from django import forms
from .models import WorkDoneModel


class WorkDoneForm(forms.ModelForm):

    class Meta:
        model = WorkDoneModel
        fields = ['title', 'content', 'tags', 'image']

    title = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),
        label='Название'
    )






