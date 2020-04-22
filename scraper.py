from bs4 import BeautifulSoup as BS
import urllib.request
import json
import concurrent.futures
import time


def get_urls_from_search_list(min_vote_count=10000):
    urls = []
    starting_position = 1
    while True:
        sauce = urllib.request.urlopen('https://www.imdb.com/search/title/'
                                       f'?title_type=tv_series&num_votes={min_vote_count},'
                                       f'&sort=num_votes,desc&start={starting_position}&ref_=adv_nxt')
        soup = BS(sauce, 'lxml')

        headers = soup.find_all('h3', {'class': 'lister-item-header'})
        # finds shows' urls and disposes of trailing trash
        current_urls = list(map(lambda p: p.find('a')['href'][:17], headers))
        urls += current_urls
        if len(current_urls) < 50:
            break
        starting_position += 50

    return urls


def get_show_data(title_url):
    print(f'Scraping: {title_url}')
    # prepares soup
    sauce = urllib.request.urlopen('https://www.imdb.com' + title_url).read()
    soup = BS(sauce, 'lxml')

    # gets info from show's main imdb page
    title = soup.find('h1').string
    original_title = soup.find('div', {'class': 'originalTitle'})  # this can return None
    poster = soup.find('div', {'class': 'poster'}).find('img')['src']
    rating = float(soup.find('span', {'itemprop': 'ratingValue'}).string)
    votes = int(soup.find('span', {'itemprop': 'ratingCount'}).string.replace(',', ''))
    season_count = int(soup.find('div', {'class': 'seasons-and-year-nav'}).find_all('div')[2].find('a').string)

    # get seasons data concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        seasons = executor.map(lambda p: get_season_data(*p), ((title_url, i) for i in range(1, season_count+1)))

    show_data = {
        'title': title,
        'original_title': original_title.text.replace(' (original title)', '') if original_title else None,
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
                'rating': float(ep.find('span', {'class': 'ipl-rating-star__rating'}).string),
                'vote_count': int(ep.find('span', {'class': 'ipl-rating-star__total-votes'}).string[1:-1].replace(',', '')),
                'thumbnail': thumb['src'],
                'air_date': ep.find('div', {'class': 'airdate'}).string.replace('\n', '')
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
    t = time.time()
    urls = load_urls_from_file('titles.txt')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        show_data = executor.map(get_show_data, urls)
    results_json = json.dumps(list(show_data))
    with open('results_json.json', 'w') as file:
        file.write(results_json)
    print(time.time()-t)


if __name__ == "__main__":
    main()
