
from rest_framework import filters, viewsets

from fetcher import serializers
from fetcher.models import tle


class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tle.TLE.objects.all()
    serializer_class = serializers.TLESerializer
    filter_fields = ('identifier',)
