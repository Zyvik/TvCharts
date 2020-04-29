from django.urls import path
from .views import TvSeriesDetail, TvSeriesList, EpisodesList, HomeView, DetailView

app_name = 'tv_charts'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>', DetailView.as_view()),
    path('api/tv_series/', TvSeriesList.as_view()),
    path('api/tv_series/<int:pk>', TvSeriesDetail.as_view()),
    path('api/tv_series/<int:pk>/episodes', EpisodesList.as_view())
]
