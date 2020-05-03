from django.test import TestCase, Client
from django.urls import reverse

from tv_charts.views import TvSeriesListDjango
from tv_charts.models import TvSeries


class TestViews(TestCase):
    client = Client()
    django_list_url = reverse('tv_charts:list')

    def test_TvSeriesListDjango_GET_valid(self):
        # Prepare simple dataset
        object_1 = TvSeries.objects.create(
            title='foo',
            imdb_url='imdb_url',
            poster_url='poster_url',
            rating=1.2,
            votes=10
        )
        object_2 = TvSeries.objects.create(
            title='bar',
            imdb_url='imdb_url',
            poster_url='poster_url',
            rating=10,
            votes=1
        )
        object_3 = TvSeries.objects.create(
            title='abc',
            imdb_url='imdb_url',
            poster_url='poster_url',
            rating=5,
            votes=2
        )

        # request with no query params - sorting by title ascending
        response = self.client.get(self.django_list_url)
        self.assertEquals(response.context['object_list'][0], object_3)

        # requests with query params
        response = self.client.get(self.django_list_url, {'starts_with': 'A'})
        self.assertEquals(response.context['object_list'][0], object_3)
        self.assertEquals(len(response.context['object_list']), 1)

        # sorting
        response = self.client.get(self.django_list_url, {'sort_by': 'votes', 'order': '-'})
        self.assertEquals(response.context['object_list'][0], object_1)

        response = self.client.get(self.django_list_url, {'sort_by': 'rating', 'order': '-'})
        self.assertEquals(response.context['object_list'][0], object_2)

        response = self.client.get(self.django_list_url, {'sort_by': 'title', 'order': '-'})
        self.assertEquals(response.context['object_list'][0], object_1)

        # per page
        response = self.client.get(self.django_list_url, {'per_page': '1'})
        self.assertEquals(len(response.context['object_list']), 1)

    def test_TvSeriesListDjango_GET_invalid(self):
        response = self.client.get(self.django_list_url, {'per_page': '0'})
        self.assertFormError(response, 'form', 'per_page', 'Ensure this value is greater than or equal to 1.')
