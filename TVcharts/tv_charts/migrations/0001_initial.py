# Generated by Django 3.0.5 on 2020-04-22 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TvSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('original_title', models.CharField(default=None, max_length=50)),
                ('imdb_url', models.CharField(max_length=100)),
                ('poster_url', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('votes', models.IntegerField()),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Episodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField()),
                ('episode_nr', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('thumbnail', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('votes', models.IntegerField()),
                ('air_date', models.CharField(max_length=50)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_charts.TvSeries')),
            ],
            options={
                'ordering': ['series', 'season', 'episode_nr'],
            },
        ),
    ]