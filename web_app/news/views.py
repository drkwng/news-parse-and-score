from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from news.models import Query, QueryCheck


class IndexView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queries'] = Query.objects.all()
        return context


class QueryView(ListView, SingleObjectMixin):
    model = QueryCheck
    template_name = 'query.html'
    ordering = '-date_check'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Query.objects.filter(pk=kwargs['pk']))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.object.querycheck_set.all()
        return super().get_queryset()
