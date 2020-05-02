from django.urls import path
from .views import TvSeriesDetail, TvSeriesList, EpisodesList, HomeView, DetailView, TvSeriesListDjango, ApiInfoView, AboutView

app_name = 'tv_charts'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>', DetailView.as_view(), name='detail'),
    path('list', TvSeriesListDjango.as_view(), name='list'),
    path('about', AboutView.as_view(), name='about'),
    path('api/', ApiInfoView.as_view(), name='api-info'),
    path('api/tv_series/', TvSeriesList.as_view(), name='api-list'),
    path('api/tv_series/<int:pk>', TvSeriesDetail.as_view(), name='api-detail'),
    path('api/tv_series/<int:pk>/episodes', EpisodesList.as_view(), name='api-episodes')
]
