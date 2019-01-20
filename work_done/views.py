
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin, TemplateView
from django.forms.models import inlineformset_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db.models import Q
from generic.controllers import PageSearchController
from generic.mixin import CurrentUrlMixin
from .models import WorkDoneModel, WorkDoneImage
from .forms import WorkDoneForm


class SearchMixin(ContextMixin):
    search = ''
    tag = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.search
        context['tag'] = self.tag
        return context


class WorkDoneListView(PageSearchController, ListView, SearchMixin, CurrentUrlMixin):
    model = WorkDoneModel
    template_name = 'work_done_list.html'
    paginate_by = 2
    allow_empty = True

    def get_queryset(self):
        project_list = super().get_queryset()
        if self.search:
            project_list = project_list.filter(Q(title__contains=self.search)
                                               | Q(content__contains=self.search))
        if self.tag:
            project_list = project_list.filter(tags__name=self.tag)
        return project_list


class WorkDoneDetailView(PageSearchController, DetailView, SearchMixin, CurrentUrlMixin):
    model = WorkDoneModel
    template_name = 'work_done_detail.html'


WorkDoneImageFormset = inlineformset_factory(WorkDoneModel, WorkDoneImage, fields=['name', 'image'], can_order=True)


class WorkDoneCreate(SuccessMessageMixin, TemplateView, CurrentUrlMixin):
    template_name = 'work_done_add.html'
    formset = None
    form = None

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.form = WorkDoneForm()
            self.formset = WorkDoneImageFormset()
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
            self.form = WorkDoneForm(request.POST, request.FILES)
            if self.form.is_valid():
                new_work_done = self.form.save()
                self.formset = WorkDoneImageFormset(request.POST, request.FILES, instance=new_work_done)
                if self.formset.is_valid():
                    self.formset.save()
                    messages.success(request, 'Новый пример выполненой работы успешно добавлен!')
                    return redirect(reverse('work_done_list') + '?search=' + new_work_done.title)
                else:
                    messages.success(request, 'Новый пример выполненой работы успешно добавлен, но фотографии не '
                                              'добавлены!')
                    return redirect(reverse('work_done_edit', kwargs={'pk': new_work_done.pk}))
            else:
                self.formset = WorkDoneImageFormset(request.POST, request.FILES)
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))


class WorkDoneUpdate(PageSearchController, TemplateView, SearchMixin, CurrentUrlMixin):
    work_done = None
    form = None
    formset = None
    template_name = 'work_done_edit.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.work_done = WorkDoneModel.objects.get(pk=self.kwargs['pk'])
            self.form = WorkDoneForm(instance=self.work_done)
            self.formset = WorkDoneImageFormset(instance=self.work_done)
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_done'] = self.work_done
        context['form'] = self.form
        context['formset'] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.work_done = WorkDoneModel.objects.get(pk=self.kwargs['pk'])
            self.form = WorkDoneForm(request.POST, request.FILES, instance=self.work_done)
            self.formset = WorkDoneImageFormset(request.POST, request.FILES, instance=self.work_done)
            if self.form.is_valid():
                self.form.save()
                if self.formset.is_valid():
                    self.formset.save()
                    messages.success(request, 'Экземляр выполненой работы успешно изменен')
                    redirect_url = reverse('work_done_list')
                    try:
                        redirect_url = redirect_url + '?page=' + self.request.GET['page']
                        try:
                            redirect_url = redirect_url + '&search' + self.request.GET['search']
                        except KeyError:
                            pass
                        try:
                            redirect_url = redirect_url + '&tag=' + self.request.GET['tag']
                        except KeyError:
                            pass
                        return redirect(redirect_url)
                    except KeyError:
                        return redirect(redirect_url)

            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))


class WorkDoneDelete(PageSearchController, TemplateView, SearchMixin):
    work_done = None
    template_name = 'work_done_delete.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.work_done = WorkDoneModel.objects.get(pk=self.kwargs['pk'])
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_done'] = self.work_done
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.work_done = WorkDoneModel.objects.get(pk=self.kwargs['pk'])
            self.work_done.delete()
            messages.success(request, 'Экземпляр выполненых работ успешно удален')
            redirect_url = reverse('work_done_list')
            try:
                redirect_url = redirect_url + '?page=' + self.request.GET['page']
                try:
                    redirect_url = redirect_url + '&search' + self.request.GET['search']
                except KeyError:
                    pass
                try:
                    redirect_url = redirect_url + '&tag=' + self.request.GET['tag']
                except KeyError:
                    pass
                return redirect(redirect_url)
            except KeyError:
                return redirect(redirect_url)
        else:
            redirect(reverse('login'))



