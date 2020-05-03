from django.test import SimpleTestCase
from django.urls import resolve, reverse

from tv_charts.views import HomeView, ApiInfoView, TvSeriesListDjango, DetailView  # Django
from tv_charts.views import TvSeriesList, TvSeriesDetail, EpisodesList  # API


class TestUrls(SimpleTestCase):
    """
    Checks if correct views are called
    """
    def test_HomeView_url(self):
        url = reverse('tv_charts:home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_ApiInfoView_url(self):
        url = reverse('tv_charts:api-info')
        self.assertEquals(resolve(url).func.view_class, ApiInfoView)

    def test_TvSeriesListDjango_url(self):
        url = reverse('tv_charts:list')
        self.assertEquals(resolve(url).func.view_class, TvSeriesListDjango)

    def test_DetailView_url(self):
        url = reverse('tv_charts:detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, DetailView)

    def test_TvSeriesList_url(self):
        url = reverse('tv_charts:api-list')
        self.assertEquals(resolve(url).func.view_class, TvSeriesList)

    def test_TvSeriesDetail_url(self):
        url = reverse('tv_charts:api-detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, TvSeriesDetail)

    def test_EpisodesList_url(self):
        url = reverse('tv_charts:api-episodes', args=[1])
        self.assertEquals(resolve(url).func.view_class, EpisodesList)
