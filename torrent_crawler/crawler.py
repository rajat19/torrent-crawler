# yts.am as of 15/04/2019

from bs4 import BeautifulSoup
import os
import re
import requests
from typing import List
from torrent_crawler.helper import update_progress


class Ratings:
    def __int__(self):
        self.rotten_tomatoes_critics = ''
        self.rotten_tomatoes_audience = ''
        self.imdb = ''

    def set_fields(self, ratings):
        if 'Rotten Tomatoes Critics - Certified Fresh' in ratings:
            self.rotten_tomatoes_critics = ratings['Rotten Tomatoes Critics - Certified Fresh']
        if 'Rotten Tomatoes Audience - Upright' in ratings:
            self.rotten_tomatoes_audience = ratings['Rotten Tomatoes Audience - Upright']
        if 'IMDb Rating' in ratings:
            self.imdb = ratings['IMDb Rating']


class Torrents:
    def __init__(self):
        self.br3d, self.br720, self.br1080, self.web720, self.web1080 = [None] * 5

    def set_fields(self, torrents):
        if '3D.BluRay' in torrents:
            self.br3d = torrents['3D.BluRay']
        if '720p.BluRay' in torrents:
            self.br720 = torrents['720p.BluRay']
        if '1080p.BluRay' in torrents:
            self.br1080 = torrents['1080p.BluRay']
        if '720p.WEB' in torrents:
            self.web720 = torrents['720p.WEB']
        if '1080p.WEB' in torrents:
            self.web1080 = torrents['1080p.WEB']


class Movie:
    header_format = 'ID|Name|Year|Link|Rotten Tomatoes Critics|Rotten Tomatoes Audience|IMDb' \
                    '|3D.BluRay|720p.BluRay|1080p.BluRay|720p.WEB|1080p.WEB\n' \
                    '---|---|---|---|---|---|---|---|---|---|---|---'
    file_name = 'movies.md'
    movie_format = '{}|{}|{}|[Link]({})|{}|{}|{}|' \
                   ' [3D.BluRay]({})|[720p.BluRay]({})|[1080p.BluRay]({})|[720p.WEB]({})|[1080p.WEB]({})'
    readme_created = True

    def __init__(self, id, name, link, year):
        self.id = id
        self.name = name
        self.link = link
        self.year = year
        self.torrents = Torrents()
        self.ratings = Ratings()
        self.subtitle_url = ''

    def save_list(self):
        exists = True
        if self.readme_created is False:
            exists = os.path.isfile(self.file_name)
        if not exists:
            self.readme_created = True
            header = self.header_format
            with open(self.file_name, 'w') as text_file:
                print(header, file=text_file)

        movie_text = self.movie_text()
        with open(self.file_name, 'a') as text_file:
            print(movie_text, file=text_file)

    def movie_text(self):
        return self.movie_format.format(
            self.id,
            self.name,
            self.year,
            self.link,
            self.ratings.rotten_tomatoes_critics,
            self.ratings.rotten_tomatoes_audience,
            self.ratings.imdb,
            self.torrents.br3d,
            self.torrents.br720,
            self.torrents.br1080,
            self.torrents.web720,
            self.torrents.web1080
        )


MoviesList = List[Movie]


class Crawler:

    list_url = 'https://yts.am/browse-movies'
    all_formats = []
    id = 1
    should_save_list = False
    should_print_to_console = False
    max_movies_in_page = 20

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
                movies_count = re.match(r'(\d+) YIFY Movies Found', movies_count_text).group(1)
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
                update_progress(current_movie_count, movies_count)
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
            movie_ratings = movie_info.find('div', {'class': 'bottom-info'}).find_all('div', {'class': 'rating-row'})
            rating_list = {}
            for rating in movie_ratings:
                rating_link = rating.find('a')
                if rating_link:
                    rater = rating_link.get('title')
                    rating_given = rating.find('span').text
                    if rater and rating_given:
                        rating_list[rater] = rating_given
            movie.torrents.set_fields(torrent_list)
            movie.ratings.set_fields(rating_list)
        elif self.should_print_to_console:
            print("{} got no info, not saving it".format(movie.name))
        movie_tech_specs = soup.find('div', {'id': 'movie-tech-specs'})
        if movie_tech_specs:
            tech_spec = movie_tech_specs.find('div', {'class': 'tech-spec-info'})
            movie.subtitle_url = tech_spec.find('a').get('href')
        return movie


if __name__ == "__main__":
    crawler = Crawler()
    crawler.should_save_list = False
    crawler.should_print_to_console = True
    movies_list = crawler.crawl_list('https://yts.am/browse-movies/american/all/all/0/latest')
    # complete_list = []
    # for movie in movies_list:
    #     complete_list.append(crawler.crawl_movie(movie['link'], movie))
    # with open("movies.json", "w") as f:
    #     json.dump(complete_list, f)
