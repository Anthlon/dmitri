from django.forms.models import modelformset_factory
from django import forms
from .models import ServiceTypeModel, ServiceModel


ServiceTypeFormset = modelformset_factory(ServiceTypeModel, fields=['name', 'order'], can_delete=True, extra=5)


class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceTypeModel
        fields = ['name', 'content']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceModel
        fields = ['name', 'content', 'service_type']


