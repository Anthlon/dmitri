from django import forms
from .models import AboutUsModel


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUsModel
        fields = ['headline', 'content']

    headline = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),
        label='Оглавление',
        help_text=''
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}),
        label='Содержание',
        help_text='',
    )

