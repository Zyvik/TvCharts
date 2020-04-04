from bs4 import BeautifulSoup as BS
import urllib.request
import json, time, concurrent.futures


def get_title_urls_from_imdb(list_url):
    sauce = urllib.request.urlopen(list_url).read()
    soup = BS(sauce, 'lxml')

    titles = soup.find_all('td', {'class': 'titleColumn'})
    links = []
    for title in titles:
        links.append(title.find('a')['href'])
    return links


def get_show_data(title_url):
    # prepare soup
    sauce = urllib.request.urlopen('https://www.imdb.com' + title_url).read()
    soup = BS(sauce, 'lxml')

    # gets info from show's main imdb page
    title = soup.find('h1').string
    poster = soup.find('div', {'class': 'poster'}).find('img')['src']
    rating = float(soup.find('span', {'itemprop': 'ratingValue'}).string)
    votes = int(soup.find('span', {'itemprop': 'ratingCount'}).string.replace(',', ''))
    season_count = int(soup.find('div', {'class': 'seasons-and-year-nav'}).find_all('div')[2].find('a').string)

    # get seasons data concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        seasons = executor.map(lambda p: get_season_data(*p), ((title_url, i) for i in range(1, season_count+1)))

    show_data = {
        'title': title,
        'imdb_url': title_url,
        'poster_url': poster,
        'rating': rating,
        'vote_count': votes,
        'seasons': list(seasons)
    }

    return show_data


def get_season_data(title_url, season_nr):
    """Returns season info - JSON style. If season isn't out yet, it returns empty list."""
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
        season_data = []
    return season_data


def read_json_file(filename):
    return json.load(open(filename))


def save_urls_to_file(url_list):
    with open('titles.txt', 'w') as file:
        for url in url_list:
            file.write(f'{url}\n')


def load_urls_from_file(filename):
    with open(filename) as file:
        urls = file.readlines()
        urls = map(lambda p: p.replace('\n', ''), urls)
    return list(urls)


urls = load_urls_from_file('titles.txt')
# t = time.time(
# print(get_show_data('/title/tt0944947/')['seasons'])
# print(time.time()-t)
# #
#
# print('Getting most popular shows...')
# popular = get_popular_tv_links('https://www.imdb.com/chart/tvmeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=7CWQMKRHYER61A9TT6CT&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_ql_5')
#
# rated = get_popular_tv_links('https://www.imdb.com/chart/toptv/?sort=nv,desc&mode=simple&page=1')
#
# links = set(popular).union(set(rated))
# links = list(links)
# print(links)
# db = []
# for index, link in enumerate(links, 1):
#     print(f'Scraping show nr: {index}/{len(links)}')
#     show_data = get_show_data(link)
#     db.append(show_data)
#     json.dump(db, open('data.txt', 'w'))
