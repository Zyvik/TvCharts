from rest_framework import serializers
from .models import TvSeries, Episodes


class TvSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvSeries
        fields = ['pk', 'title', 'original_title', 'imdb_url', 'poster_url', 'rating', 'votes']


class EpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodes
        fields = ['pk', 'series', 'season', 'episode_nr', 'title', 'thumbnail', 'rating', 'votes', 'air_date']
