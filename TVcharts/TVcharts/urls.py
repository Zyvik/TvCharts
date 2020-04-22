from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tv_charts.urls', namespace='tv_charts'))
]
