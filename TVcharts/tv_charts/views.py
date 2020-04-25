from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import TvSeries
from . serializers import TvSeriesSerializer


class TvSeriesList(APIView):
    """
    List all TV series
    """
    def get(self, request, format=None):
        series = TvSeries.objects.all()
        serializer = TvSeriesSerializer(series, many=True)
        return Response(serializer.data)


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
