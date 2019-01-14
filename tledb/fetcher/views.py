
from django.views.generic.list import ListView

import django_tables2 as tables
from rest_framework import filters, viewsets

from fetcher import serializers
from fetcher.models import tle


class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    """REST"""
    queryset = tle.TLE.objects.all()
    serializer_class = serializers.TLESerializer
    filter_fields = ('identifier',)


class TLEListView(ListView):
    """View to list the TLE objects from the database"""
    model = tle.TLE
    template_name = 'tle_list.html'


class TLETable(tables.Table):
    class Meta:
        model = tle.TLE
        exclude = ('id',)
        template_name = 'django_tables2/bootstrap.html'


class TLETableView(tables.SingleTableView):
    table_class = TLETable
    queryset = tle.TLE.objects.all()
    template_name = "tle_list.html"
