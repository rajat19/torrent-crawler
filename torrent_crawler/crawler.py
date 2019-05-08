# yts.am as of 15/04/2019

from bs4 import BeautifulSoup
import os
import re
import requests
from torrent_crawler.progress_bar import ProgressBar


class Crawler:

    list_url = 'https://yts.am/browse-movies'
    header_format = 'ID|Name|Year|Link|Rotten Tomatoes Critics|Rotten Tomatoes Audience|IMDb' \
                    '|3D.BluRay|720p.BluRay|1080p.BluRay|720p.WEB|1080p.WEB\n' \
                    '---|---|---|---|---|---|---|---|---|---|---|---'
    movie_format = '{}|{}|{}|[Link]({})|{}|{}|{}|' \
                   ' [3D.BluRay]({})|[720p.BluRay]({})|[1080p.BluRay]({})|[720p.WEB]({})|[1080p.WEB]({})'
    file_name = 'movies.md'
    all_formats = []
    readme_created = True
    id = 1
    should_save_list = False
    should_print_to_console = False
    max_movies_in_page = 20

    @staticmethod
    def fill_non_existing(movie):
        if 'ratings' not in movie:
            movie['ratings'] = {}
        if 'torrents' not in movie:
            movie['torrents'] = {}
        movie_ratings = movie['ratings']
        movie_torrents = movie['torrents']
        if 'Rotten Tomatoes Critics - Certified Fresh' not in movie_ratings:
            movie['ratings']['Rotten Tomatoes Critics - Certified Fresh'] = ''
        if 'Rotten Tomatoes Audience - Upright' not in movie_ratings:
            movie['ratings']['Rotten Tomatoes Audience - Upright'] = ''
        if 'IMDb Rating' not in movie_ratings:
            movie['ratings']['IMDb Rating'] = ''

        if '3D.BluRay' not in movie_torrents:
            movie['torrents']['3D.BluRay'] = ''
        if '720p.BluRay' not in movie_torrents:
            movie['torrents']['720p.BluRay'] = ''
        if '1080p.BluRay' not in movie_torrents:
            movie['torrents']['1080p.BluRay'] = ''
        if '720p.WEB' not in movie_torrents:
            movie['torrents']['720p.WEB'] = ''
        if '1080p.WEB' not in movie_torrents:
            movie['torrents']['1080p.WEB'] = ''
        return movie

    def save_list(self, movie):
        exists = True
        if self.readme_created is False:
            exists = os.path.isfile(self.file_name)
        if not exists:
            self.readme_created = True
            header = self.header_format
            with open(self.file_name, 'w') as text_file:
                print(header, file=text_file)

        movie = self.fill_non_existing(movie)
        movie_text = self.movie_format.format(
            self.id,
            movie['name'],
            movie['year'],
            movie['link'],
            movie['ratings']['Rotten Tomatoes Critics - Certified Fresh'],
            movie['ratings']['Rotten Tomatoes Audience - Upright'],
            movie['ratings']['IMDb Rating'],
            movie['torrents']['3D.BluRay'],
            movie['torrents']['720p.BluRay'],
            movie['torrents']['1080p.BluRay'],
            movie['torrents']['720p.WEB'],
            movie['torrents']['1080p.WEB']
        )
        with open(self.file_name, 'a') as text_file:
            print(movie_text, file=text_file)
        self.id += 1

    def crawl_list(self, crawl_url):
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
                movie = {
                    'name': movie_name,
                    'link': movie_link,
                    'year': int(movie_year)
                }
                movie = self.crawl_movie(movie_link, movie)
                movies.append(movie)
                if self.should_print_to_console:
                    print('{}: {}'.format(current_movie_count, movie_name))
                if self.should_save_list:
                    self.save_list(movie)
                ProgressBar.update_progress(current_movie_count, movies_count)
                current_movie_count += 1
            page_no += 1
        return movies

    def crawl_movie(self, movie_link, movie_details):
        req = requests.get(movie_link)
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
            movie_details['torrents'] = torrent_list
            movie_details['ratings'] = rating_list
        elif self.should_print_to_console:
            print("{} got no info, not saving it".format(movie_details['name']))
        return movie_details


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
