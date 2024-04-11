from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Comment, Bill
from django_filters import FilterSet, ModelChoiceFilter


class BillFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ['comment_bill']

    def __init__(self, *args, **kwargs):
        super(BillFilter, self).__init__(*args, **kwargs)
        self.filters['comment_bill'].queryset = Bill.objects.filter(author__id=kwargs['request'])
