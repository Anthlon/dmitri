from django.views.generic.base import View


class PageSearchController(View):
    """Назначение

    1. Получает номер страницы и добавляет его к интернет-адресу переадресации
    после успешного сохранения или удаления записи.
    """
    def get(self, request, *args, **kwargs):
        try:
            self.search = self.request.GET['search']
        except KeyError:
            self.search = ''
        try:
            self.tag = self.request.GET['tag']
        except KeyError:
            self.tag = ''
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        try:
            pn = request.GET['page']
        except KeyError:
            pn = '1'
        self.success_url = self.success_url + "?page=" + pn
        try:
            self.success_url = self.success_url + '&search=' + request.GET['search']
        except KeyError:
            pass
        try:
            self.success_url = self.success_url + '&tag=' + request.GET['tag']
        except KeyError:
            pass
        return super().post(request, *args, **kwargs)

