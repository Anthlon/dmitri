
from .models import ServiceTypeModel, ServiceModel
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ServiceTypeFormset, ServiceTypeForm, ServiceForm


class ServiceTypeEdit(TemplateView):
    template_name = 'service_type_edit.html'
    formset = None

    def get(self, request, *args, **kwargs):
        self.formset = ServiceTypeFormset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.formset = ServiceTypeFormset(request.POST)
        if self.formset.is_valid():
            self.formset.save()
            messages.success(request, 'Перечень категорий услуг успешно изменен')
            return redirect('service_type_edit')
        else:
            return super().get(request, *args, **kwargs)


class ServiceMainView(TemplateView):
    template_name = 'service_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_types'] = ServiceTypeModel.objects.order_by('order')
        return context


class ServiceTypeView(DetailView):
    template_name = 'service_type.html'
    model = ServiceTypeModel


class ServiceTypeSingleEdit(TemplateView):
    service_type = None
    form = None
    template_name = 'service_type_single_edit.html'

    def get(self, request, *args, **kwargs):
        self.service_type = ServiceTypeModel.objects.get(pk=self.kwargs['pk'])
        self.form = ServiceTypeForm(instance=self.service_type)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.service_type = ServiceTypeModel.objects.get(pk=self.kwargs['pk'])
        self.form = ServiceTypeForm(request.POST, instance=self.service_type)
        if self.form.is_valid():
            new = self.form.save()
            messages.success(request, 'Категория услуги успешно сохранена.')
            return redirect(reverse('service_type', kwargs={'pk': new.pk}))
        else:
            return super().get(request, *args, **kwargs)


class ServiceAdd(TemplateView):
    template_name = 'service_add.html'
    form = None
    cat = None

    def get(self, request, *args, **kwargs):
        try:
            self.cat = ServiceTypeModel.objects.get(pk=self.request.GET['cat'])
        except KeyError:
            self.cat = ServiceTypeModel.objects.first()
        self.form = ServiceForm(initial={'service_type': self.cat})
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.form = ServiceForm(request.POST)
        if self.form.is_valid():
            new = self.form.save()
            messages.success(request, 'Услуга добавлена успешно')
            return redirect(reverse('service_type', kwargs={'pk': new.service_type.pk}))
        return super().get(request, *args, **kwargs)


class ServiceView(DetailView):
    template_name = 'service.html'
    model = ServiceModel


class ServiceEdit(UpdateView):
    model = ServiceModel
    template_name = 'service_edit.html'
    fields = ['name', 'content']

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('service_type',
                                   kwargs={'pk': ServiceModel.objects.get(pk=kwargs['pk']).service_type.pk})
        messages.success(request, 'Услуга успешно сохранена.')
        return super().post(request, *args, **kwargs)


class ServiceDelete(DeleteView):
    model = ServiceModel
    template_name = 'service_delete.html'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('service_type',
                                   kwargs={'pk': ServiceModel.objects.get(pk=kwargs['pk']).service_type.pk})
        messages.success(request, 'Услуга успешно удалена')
        return super().post(request, *args, **kwargs)



