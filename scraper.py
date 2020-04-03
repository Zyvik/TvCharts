from bs4 import BeautifulSoup as BS
import urllib.request


def get_popular_tv_links():
    sauce = urllib.request.urlopen('https://www.imdb.com/chart/toptv/?sort=nv,desc&mode=simple&page=1').read()
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

    get_episodes_data(title_url, 1)
    show_data = {
        'title': title,
        'poster_url': poster,
        'rating': rating,
        'vote_count': votes,
        'episodes': ''
    }

    return show_data


def get_episodes_data(title_url, season_nr):
    sauce = urllib.request.urlopen(f'https://www.imdb.com{title_url}episodes?season={season_nr}')
    soup = BS(sauce, 'lxml')

    episodes = soup.find_all('div', {'class': 'info', 'itemprop': 'episodes'})
    thumbnails = soup.find_all('img', {'class': 'zero-z-index'})

    season_data = {}
    for ep, thumb, i in zip(episodes, thumbnails, range(len(episodes))):
        episode_data = {
            'title': ep.find('a', {'itemprop': 'name'}).string,
            'rating': ep.find('span', {'class': 'ipl-rating-star__rating'}).string,
            'votes': ep.find('span', {'class': 'ipl-rating-star__total-votes'}).string,
            'thumbnail': thumb['src']
        }
        season_data[i+1] = episode_data

    print(season_data)

links = get_popular_tv_links()
get_show_data(links[0])