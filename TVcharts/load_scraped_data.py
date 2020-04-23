import os
import re
import datetime
import django
import json
os.environ["DJANGO_SETTINGS_MODULE"] = 'TVcharts.settings'
django.setup()
from tv_charts.models import TvSeries, Episodes


def clean_title(dirty_title):
    """ Title comes in like this: 'Foobar\u00a0            '."""
    return dirty_title.split('\u00a0')[0]


def clean_air_date(dirty_date):
    """Air date comes in like this: '            26 Feb. 2004    '."""
    pattern = re.compile(r'\d+ .{3,4} \d{4}')
    match = pattern.search(dirty_date)
    if match:
        air_date_string = match.group().replace('.', '')  # '26 Feb 2004'
        return datetime.datetime.strptime(air_date_string, '%d %b %Y').date()
    return None


def create_tv_series(tv_dict):
    series_model = TvSeries(
        title=clean_title(tv_dict['title']),
        original_title=tv_dict['original_title'],
        imdb_url=tv_dict['imdb_url'],
        poster_url=tv_dict['poster_url'],
        rating=tv_dict['rating'],
        votes=tv_dict['vote_count']
    )
    series_model.save()
    return series_model


def create_episode(series, season_nr, episode_dict, episode_nr):
    episode = Episodes(
        series=series,
        season=season_nr,
        episode_nr=episode_nr,
        title=episode_dict['title'],
        thumbnail=episode_dict['thumbnail'],
        rating=episode_dict['rating'],
        votes=episode_dict['vote_count'],
        air_date=clean_air_date(episode_dict['air_date'])
    )
    episode.save()


def create_data(path='scraped data/'):
    data = []
    for directory in os.listdir(path):
        if directory.endswith('.json'):
            with open(path + directory) as file:
                data += json.load(file)
    return data


def save_data_to_db(data):
    for data_index, tv_dict in enumerate(data):
        current_series = create_tv_series(tv_dict)
        for season_nr, episodes_list in enumerate(tv_dict['seasons'], 1):
            for episode_nr, episode_dict in enumerate(episodes_list, 1):
                create_episode(
                    series=current_series,
                    season_nr=season_nr,
                    episode_dict=episode_dict,
                    episode_nr=episode_nr
                )
        if data_index % 10 == 0:
            print(f'Processing... {data_index}/{len(data)}')


def drop_tv_charts_db():
    TvSeries.objects.all().delete()


def main():
    data = create_data()
    drop_tv_charts_db()
    save_data_to_db(data)
    print('Done')


if __name__ == '__main__':
    main()
