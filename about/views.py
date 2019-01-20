
from django.views.generic.base import TemplateView
from generic.mixin import CurrentUrlMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import AboutUsForm
from django.contrib import messages
from django.forms.models import inlineformset_factory
from .models import AboutUsModel, PreviousEmployment


AboutUsFormset = inlineformset_factory(AboutUsModel, PreviousEmployment,
                                       fields=['organization', 'post', 'content', 'date_start', 'date_end'])


def about_data():
    """
    Ensures the use of a single instance of the model.
    If there is no instance of the model, it creates it.

    :return: Single object AboutUsModel
    """
    if not AboutUsModel.objects.exists():
        AboutUsModel.objects.create(headline='Заголовок', content='Содержание')
    return AboutUsModel.objects.first()


class AboutUsView(CurrentUrlMixin, TemplateView):
    about_data = None
    template_name = 'about_us.html'

    def get(self, request, *args, **kwargs):
        self.about_data = about_data()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_data'] = self.about_data
        context['employments'] = PreviousEmployment.objects.all()
        return context


class AboutEdit(CurrentUrlMixin, TemplateView):
    form = None
    formset = None
    template_name = 'about_edit.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.form = AboutUsForm(instance=about_data())
            self.formset = AboutUsFormset(instance=about_data())
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.form = AboutUsForm(request.POST, instance=about_data())
            if self.form.is_valid():
                new = self.form.save()
                self.formset = AboutUsFormset(request.POST, instance=new)
                messages.success(request, 'Изменения статьи "о себе" успешно сохранены.')
                if self.formset.is_valid():
                    self.formset.save()
                    messages.success(request, 'Изменения мест работы успешно сохранены.')
                    return redirect(reverse('about_us'))
                else:
                    messages.success(request, 'Изменения мест работы не сохранены.')

            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))


