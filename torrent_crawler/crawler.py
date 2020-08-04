# yts.am as of 15/04/2019

from bs4 import BeautifulSoup
import re
import requests
from typing import List
from torrent_crawler.helper import Helper
from torrent_crawler.models import Movie


MoviesList = List[Movie]


class Crawler:
    def __init__(self, api_flag=False, save_list=False, print_console=False):
        self.api_flag = api_flag
        self.list_url = 'https://yts.am/browse-movies'
        self.all_formats = []
        self.id = 1
        self.should_save_list = save_list or False
        self.should_print_to_console = print_console or False
        self.max_movies_in_page = 20
        self.update_progress = False if api_flag is True else True

    def crawl_list(self, crawl_url: str) -> MoviesList:
        page_no = 1
        has_next_page = True
        movies = []
        current_movie_count = 1
        movies_count = 0
        while has_next_page:
            if not crawl_url:
                crawl_url = self.list_url
            request_url = crawl_url
            if page_no > 1:
                request_url = '{0}?page={1}'.format(crawl_url, page_no)
            req = requests.get(request_url)
            soup = BeautifulSoup(req.text, features='html5lib')
            if page_no == 1:
                movies_count_text = soup.find('div', {'class': 'browse-content'}).find('h2').text
                movies_count_text = movies_count_text.replace(',', '')
                movies_count = re.match(r'(\d+) YIFY Movies found', movies_count_text).group(1)
                movies_count = int(movies_count)
                print('Total {} movies found'.format(movies_count))
            movie_wraps = soup.find_all('div', {'class': 'browse-movie-wrap'})
            if len(movie_wraps) < self.max_movies_in_page:
                has_next_page = False
            for wrap in movie_wraps:
                movie_link = wrap.find('a', {'class': 'browse-movie-link'}).get('href')
                movie_details = wrap.find('div', {'class': 'browse-movie-bottom'})
                movie_name = movie_details.find('a', {'class': 'browse-movie-title'}).text
                movie_year = movie_details.find('div', {'class': 'browse-movie-year'}).text
                # TODO: find and use movie tags
                movie = Movie(current_movie_count, movie_name, movie_link, int(movie_year))
                movie = self.crawl_movie(movie)
                movies.append(movie)
                if self.should_print_to_console:
                    print('{}: {}'.format(current_movie_count, movie_name))
                if self.should_save_list:
                    movie.save_list()
                if self.update_progress:
                    Helper.update_progress(current_movie_count, movies_count)
                current_movie_count += 1
            page_no += 1
        return movies

    def crawl_movie(self, movie: Movie) -> Movie:
        req = requests.get(movie.link)
        soup = BeautifulSoup(req.text, features='html5lib')
        movie_info = soup.find('div', {'id': 'movie-info'})
        if movie_info:
            # TODO: find and use movie genres
            movie_torrents = movie_info.find('p', {'class': 'hidden-xs hidden-sm'}).find_all('a')
            torrent_list = {}
            for torrent in movie_torrents:
                torrent_link = torrent.get('href')
                torrent_quality = torrent.text
                if torrent_link and torrent_quality:
                    torrent_list[torrent_quality] = torrent_link
            movie_ratings = movie_info.find('div', {'class': 'bottom-info'}).find_all('div', {'itemprop': 'aggregateRating'})
            rating_list = {}
            for rating in movie_ratings:
                rating_link = rating.find('a')
                if rating_link:
                    rater = rating_link.get('title')
                    r = rating.find('span', {'itemprop': 'ratingValue'})
                    rating_given = rating.find('span', {'itemprop': 'ratingValue'}).text
                    if rater and rating_given:
                        rating_list[rater] = rating_given
            movie.set_torrents(torrent_list)
            movie.set_ratings(rating_list)
        elif self.should_print_to_console:
            print("{} got no info, not saving it".format(movie.name))
        movie_tech_specs = soup.find('div', {'id': 'movie-tech-specs'})
        if movie_tech_specs:
            tech_spec = movie_tech_specs.find('div', {'class': 'tech-spec-info'})
            subtitle_url = tech_spec.find('a')
            if subtitle_url:
                movie.subtitle_url = subtitle_url.get('href')
        return movie


if __name__ == "__main__":
    crawler = Crawler()
    crawler.should_save_list = False
    crawler.should_print_to_console = True
    movies_list = crawler.crawl_list('https://yts.mx/browse-movies/avenger/all/all/0/latest/0/all')
    # complete_list = []
    # for movie in movies_list:
    #     complete_list.append(crawler.crawl_movie(movie['link'], movie))
    # with open("movies.json", "w") as f:
    #     json.dump(complete_list, f)
