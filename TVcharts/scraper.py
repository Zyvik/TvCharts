from urllib import request, error
import json
import concurrent.futures
from bs4 import BeautifulSoup as BS


def get_urls_from_search_list(min_vote_count=10000):
    urls = []
    starting_position = 1
    # most popular tv shows (# of votes)
    url = 'https://www.imdb.com/search/title/'\
          f'?title_type=tv_series&num_votes={min_vote_count},'\
          f'&sort=num_votes,desc&start={starting_position}&ref_=adv_nxt'

    while True:
        sauce = request.urlopen(url)
        soup = BS(sauce, 'lxml')

        headers = soup.find_all('h3', {'class': 'lister-item-header'})
        # finds shows' urls and disposes of trailing trash
        current_urls = list(map(lambda p: p.find('a')['href'][:17], headers))
        urls += current_urls
        starting_position += 50
        if len(current_urls) < 50:
            break

    return urls


def get_show_data(title_url):
    # prepares soup
    sauce = request.urlopen('https://www.imdb.com' + title_url).read()
    soup = BS(sauce, 'lxml')

    # gets info from show's main imdb page
    title = soup.find('h1').string
    original_title = soup.find('div', {'class': 'originalTitle'})
    poster = soup.find('div', {'class': 'poster'}).find('img')['src']
    rating = float(soup.find('span', {'itemprop': 'ratingValue'}).string)
    votes = int(soup.find('span', {'itemprop': 'ratingCount'}).string.replace(',', ''))
    try:
        seasons_div = soup.find('div', {'class': 'seasons-and-year-nav'})
        season_count = int(seasons_div.find_all('div')[2].find('a').string)

        # get seasons data concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            seasons = executor.map(
                lambda p: get_season_data(*p),
                ((title_url, i) for i in range(1, season_count + 1))
            )
    except IndexError:
        seasons = ''

    show_data = {
        'title': title,
        'original_title': original_title,
        'imdb_url': title_url,
        'poster_url': poster,
        'rating': rating,
        'vote_count': votes,
        'seasons': list(seasons)
    }

    return show_data


def get_season_data(title_url, season_nr):
    """Returns season info. If season isn't out yet, it returns empty list."""
    try:
        url = f'https://www.imdb.com{title_url}episodes?season={season_nr}'
        sauce = request.urlopen(url)
    except error.HTTPError:
        return []
    soup = BS(sauce, 'lxml')

    episodes = soup.find_all('div', {'class': 'info', 'itemprop': 'episodes'})
    thumbnails = soup.find_all('img', {'class': 'zero-z-index'})
    season_data = []

    try:
        for ep, thumb, i in zip(episodes, thumbnails, range(len(episodes))):
            rating_div = ep.find('span', {'class': 'ipl-rating-star__rating'})
            votes = ep.find('span', {'class': 'ipl-rating-star__total-votes'})
            air_date_div = ep.find('div', {'class': 'airdate'})
            episode_data = {
                'title': ep.find('a', {'itemprop': 'name'}).string,
                'rating': float(rating_div.string),
                'vote_count': int(votes.string[1:-1].replace(',', '')),
                'thumbnail': thumb['src'],
                'air_date': air_date_div.string.replace('\n', '')
            }

            season_data.append(episode_data)
    except AttributeError:
        season_data = []

    return season_data


def save_urls_to_file(url_list, filename):
    with open(filename, 'w') as file:
        for url in url_list:
            file.write(f'{url}\n')


def load_urls_from_file(filename):
    with open(filename) as file:
        urls = file.readlines()
        urls = map(lambda p: p.replace('\n', ''), urls)
    return list(urls)


def main():
    results_step = 100
    urls = load_urls_from_file('titles.txt')
    for i in range(0, len(urls), results_step):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            show_data = executor.map(get_show_data, urls[i:i+results_step])
        results_json = json.dumps(list(show_data))
        if results_json:
            with open(f'results_{i}.json', 'w') as file:
                file.write(results_json)


if __name__ == "__main__":
    main()
