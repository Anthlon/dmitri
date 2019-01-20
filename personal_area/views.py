

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from generic.mixin import CurrentUrlMixin
from feedback.models import FeedbackModel
from .models import CustomUser


class PersonalArea(CurrentUrlMixin, ListView):
    allow_empty = True
    template_name = 'personal_area.html'
    paginate_by = 5
    model = FeedbackModel

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse('feedback'))


class ClientRequestDetail:
    pass


class UserListView(CurrentUrlMixin, ListView):
    allow_empty = True
    paginate_by = 5
    template_name = 'user_list.html'
    user_list = None

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.user_list = CustomUser.objects.all().order_by('-date_joined')
        else:
            return redirect(reverse('login'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.user_list


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user_detail_view.html'
    paginator = None
    page_num = 1

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            redirect(reverse('login'))
        else:
            if not self.kwargs['pk']:
                redirect(reverse('user_list'))
            else:
                pk = kwargs['pk']
                user = self.model.objects.get(pk=pk)
                self.paginator = Paginator(FeedbackModel.objects.filter(user=user).order_by('-date_time_post'), 5)

        self.page_num = request.GET.get('page')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page_obj = self.paginator.page(self.page_num)
        except InvalidPage:
            page_obj = self.paginator.page(1)
        context['paginator'] = self.paginator
        context['page_obj'] = page_obj
        return context


