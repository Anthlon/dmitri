
from django.views.generic.base import ContextMixin


class CurrentUrlMixin(ContextMixin):
    """Назначение

    1. Помещает номер страницы в особую переменную контекста данных
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_url'] = self.request.path
        return context
