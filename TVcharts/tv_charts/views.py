from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters

from .models import TvSeries
from . serializers import TvSeriesSerializer


class TvSeriesList(generics.ListAPIView):
    """
    List all TV series
    """
    search_fields = ['title', 'original_title']
    filter_backends = (filters.SearchFilter,)
    queryset = TvSeries.objects.all()
    serializer_class = TvSeriesSerializer


class TvSeriesDetail(APIView):
    """
    Retrieve specific TvSeries instance
    """
    def get(self, request, pk, format=None):
        try:
            series = TvSeries.objects.get(pk=pk)
        except TvSeries.DoesNotExists:
            raise Http404
        serializer = TvSeriesSerializer(series)
        return Response(serializer.data)

