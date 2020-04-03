from bs4 import BeautifulSoup as BS
import urllib.request
import json


def get_popular_tv_links(list_url):
    sauce = urllib.request.urlopen(list_url).read()
    soup = BS(sauce, 'lxml')

    titles = soup.find_all('td', {'class': 'titleColumn'})
    links = []
    for title in titles:
        links.append(title.find('a')['href'])
    return links


def get_show_data(title_url):
    sauce = urllib.request.urlopen('https://www.imdb.com' + title_url).read()
    soup = BS(sauce, 'lxml')

    title = soup.find('h1').string
    poster = soup.find('div', {'class': 'poster'}).find('img')['src']
    rating = float(soup.find('span', {'itemprop': 'ratingValue'}).string)
    votes = int(soup.find('span', {'itemprop': 'ratingCount'}).string.replace(',', ''))

    seasons = []
    previous_season = 'dummy data'
    for i in range(0, 40):
        current_season = get_season_data(title_url, i)
        # if you want to get season that doesnt exist, you will get the latest season
        # some seasons don't have info because they aren't out yet
        if current_season == previous_season or not current_season:
            break
        seasons.append(current_season)
        previous_season = current_season

    show_data = {
        'title': title,
        'imdb_url': title_url,
        'poster_url': poster,
        'rating': rating,
        'vote_count': votes,
        'seasons': seasons
    }

    return show_data


def get_season_data(title_url, season_nr):
    """Returns season info - JSON style. If season isn't out yet, it returns empty dict."""
    sauce = urllib.request.urlopen(f'https://www.imdb.com{title_url}episodes?season={season_nr}')
    soup = BS(sauce, 'lxml')

    episodes = soup.find_all('div', {'class': 'info', 'itemprop': 'episodes'})
    thumbnails = soup.find_all('img', {'class': 'zero-z-index'})
    season_data = []

    try:
        for ep, thumb, i in zip(episodes, thumbnails, range(len(episodes))):
            episode_data = {
                'title': ep.find('a', {'itemprop': 'name'}).string,
                'rating': ep.find('span', {'class': 'ipl-rating-star__rating'}).string,
                'votes': ep.find('span', {'class': 'ipl-rating-star__total-votes'}).string,
                'thumbnail': thumb['src']
            }
            season_data.append(episode_data)
    except AttributeError:
        season_data = {}
    return season_data

#

print('Getting most popular shows...')
popular = get_popular_tv_links('https://www.imdb.com/chart/tvmeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=7CWQMKRHYER61A9TT6CT&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_ql_5')

rated = get_popular_tv_links('https://www.imdb.com/chart/toptv/?sort=nv,desc&mode=simple&page=1')

links = set(popular).union(set(rated))
links = list(links)
print(links)
db = []
for index, link in enumerate(links, 1):
    print(f'Scraping show nr: {index}/{len(links)}')
    show_data = get_show_data(link)
    db.append(show_data)
    json.dump(db, open('data.txt', 'w'))
