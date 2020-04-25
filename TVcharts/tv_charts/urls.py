from django.urls import path
from .views import TvSeriesDetail, TvSeriesList

app_name = 'tv_charts'
urlpatterns = [
    path('api/tv_series/', TvSeriesList.as_view()),
    path('api/tv_series/<int:pk>', TvSeriesDetail.as_view())
]
