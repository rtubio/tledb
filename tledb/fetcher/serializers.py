
from fetcher.models import tle
from rest_framework import serializers


class TLESerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tle.TLE
        fields = (
            'identifier', 'timestamp', 'source', 'first_line', 'second_line'
        )
