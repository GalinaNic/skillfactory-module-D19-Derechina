from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from bills.models import Comment, Bill
from django_filters import FilterSet, ModelChoiceFilter


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Comment.objects.filter(comment_bill__author__id=self.request.user.id)
        context['filterset'] = BillFilter(self.request.GET, request=self.request.user.id)
        return context