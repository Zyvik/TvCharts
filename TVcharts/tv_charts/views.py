from django.http import Http404
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters

from .models import TvSeries, Episodes
from .serializers import TvSeriesSerializer, EpisodesSerializer
from .forms import FilterForm


class HomeView(generic.TemplateView):
    """
    Landing page - with search option
    """
    template_name = 'tv_charts/tvseries_home.html'


class TvSeriesListDjango(generic.list.ListView):
    """
    List view with filter option
    """
    model = TvSeries
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        queryset = queryset.order_by('title')

        form = FilterForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('starts_with')
            if title:
                queryset = queryset.filter(title__startswith=title)

            sort = form.cleaned_data.get('sort_by')
            order = form.cleaned_data.get('order', '')
            if sort:
                queryset = queryset.order_by(f'{order}{sort}')

            per_page = form.cleaned_data.get('per_page')
            if per_page:
                self.paginate_by = int(per_page)
        return super().get_context_data(object_list=queryset, form=form)


class DetailView(generic.detail.DetailView):
    """
    TvSeries detail view - with chart containing all episodes (episodes data are taken from API)
    """
    model = TvSeries


class ApiInfoView(generic.TemplateView):
    """
    Contains info about "API"
    """
    template_name = 'tv_charts/API.html'


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


class EpisodesList(APIView):
    """
    List all episodes from TvSeries instance
    """
    def get(self, request, pk, format=None):
        try:
            series = TvSeries.objects.get(pk=pk)
        except TvSeries.DoesNotExists:
            raise Http404

        episodes = Episodes.objects.filter(series=series)
        serializer = EpisodesSerializer(episodes, many=True)
        return Response(serializer.data)
