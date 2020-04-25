from rest_framework import serializers
from .models import TvSeries


class TvSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvSeries
        fields = ['pk', 'title', 'original_title', 'imdb_url', 'poster_url', 'rating', 'votes']
