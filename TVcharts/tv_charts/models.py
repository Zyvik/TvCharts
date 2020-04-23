from django.db import models


# Create your models here.
class TvSeries(models.Model):
    title = models.CharField(max_length=50)
    original_title = models.CharField(max_length=50, default=None, null=True)
    imdb_url = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=100)
    rating = models.DecimalField(decimal_places=1, max_digits=3)
    votes = models.IntegerField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Episodes(models.Model):
    series = models.ForeignKey(TvSeries, models.CASCADE)
    season = models.IntegerField()
    episode_nr = models.IntegerField()
    title = models.CharField(max_length=50)
    thumbnail = models.CharField(max_length=100)
    rating = models.DecimalField(decimal_places=1, max_digits=3)
    votes = models.IntegerField()
    air_date = models.DateField(null=True)

    class Meta:
        ordering = ['series', 'season', 'episode_nr']

    def __str__(self):
        return f'{self.series} s{self.season}e{self.episode_nr}'
