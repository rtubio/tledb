
from django.views.generic.list import ListView

from rest_framework import filters, viewsets

from fetcher import serializers
from fetcher.models import tle


class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tle.TLE.objects.all()
    serializer_class = serializers.TLESerializer
    filter_fields = ('identifier',)


class TLEListView(ListView):
    """View to list the TLE objects from the database"""
    model = tle.TLE
    template_name = 'tle_list.html'
