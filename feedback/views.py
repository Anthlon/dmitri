
from django.views.generic.base import TemplateView
from .forms import FeedbackForm
from generic.mixin import CurrentUrlMixin
from .models import FeedbackModel, DefenderModel
from django.contrib import messages
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone


def excess(ip):
    """

    :param ip-address guest how post request
    :return: DefenderModel.object
    """
    try:
        member = DefenderModel.objects.get(ip_address=ip)
    except DefenderModel.DoesNotExist:
        member = DefenderModel(ip_address=ip)

    member.total_counter += 1
    member.counter += 1

    if not member.excess:
        print(member.banned_dt)
        if timezone.now() > member.banned_dt:
            member.excess = True
            member.save()
            return member
        else:
            return member

    if member.total_counter > 100:
        member.excess = False
        member.banned_dt = timezone.now() + timedelta(days=30)
        member.counter = 0
        member.save()
        return member

    if member.counter > 3:
        if member.counter > 10 or len(FeedbackModel.objects.filter(member=member)) > 3:
            member.excess = False
            member.banned_dt = timezone.now() + timedelta(days=1)
            member.counter = 0
            member.save()
            return member

    member.save()
    return member


class FeedbackView(CurrentUrlMixin, TemplateView):
    """Назначение

    Выводит форму обратной связи.
    Выводит для авторизованных пользователей последние сообщения
    """
    form = None
    feedback_list = None
    template_name = 'feedback.html'
    ip_address = None
    msg = 'Ваша заявка успешно принята! '

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.feedback_list = FeedbackModel.objects.filter(user=request.user)[:3]
            self.form = FeedbackForm({'name': request.user.first_name + ' ' + request.user.last_name,
                                      'content': 'У нас есть для вас работа!',
                                      'email': request.user.email})
        else:
            self.form = FeedbackForm()

        for field in self.form.visible_fields():
            print(field.field.widget.template_name)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.feedback_list:
            context['feedback_list'] = self.feedback_list
        return context

    def post(self, request, *args, **kwargs):
        self.form = FeedbackForm(request.POST)

        if not request.user.is_staff:
            member = excess(request.META["REMOTE_ADDR"])
            if not member.excess:
                return render(request, 'sorry.html')
            else:
                self.form.instance.member = member

        if request.user.is_authenticated:
            self.form.user_is_authenticated = True
            self.feedback_list = FeedbackModel.objects.filter(user=request.user)
            self.form.instance.user = request.user
        else:
            self.msg = self.msg + 'Проверьте вашу почту, вам отправлено автоматическое сообщение. Если оно не ' \
                                  'пришло значит вы неверно указали адрес электронной почты.'

        if self.form.is_valid():
            client_request = self.form.save()
            messages.success(request, self.msg)
            return render(request, 'thank_you.html', {'client_request': client_request,
                                                      'current_url': self.get_context_data()['current_url']})
        return super().get(request, *args, **kwargs)



