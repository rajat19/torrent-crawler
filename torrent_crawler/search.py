import signal
import traceback
from typing import Dict, List
from torrent_crawler.constants import Constants
from torrent_crawler.color import Color
from torrent_crawler.crawler import Crawler
from torrent_crawler.helper import Helper
from torrent_crawler.models import Movie, Torrents
from torrent_crawler.print import Print
from torrent_crawler.subtitle import Subtitle


def sigint_handler(signum, frame):
    Print.thanks()
    exit(1)


signal.signal(signal.SIGINT, sigint_handler)


class SearchQuery:
    def __init__(self, search_term, quality, genre, rating, order_by, year=0, language='en'):
        self.search_term = search_term
        self.quality = quality
        self.genre = genre
        self.rating = rating
        self.order_by = order_by
        self.language = language
        self.year = year

    def get_url(self):
        return Constants.search_url.format(self.search_term, self.quality, self.genre,
                                           self.rating, self.order_by, self.year, self.language)


class Search:
    def __init__(self, search_query: SearchQuery, api_flag: bool = False):
        self.search_query = search_query
        self.api_flag = api_flag

    def get_available_torrents(self, torrents: Torrents) -> Dict:
        available_torrents = {}
        if self.search_query.quality in ['all', '3D'] and torrents.br3d:
            available_torrents['3D.BluRay'] = torrents.br3d
        if self.search_query.quality in ['all', '720'] and torrents.br720:
            available_torrents['720p.BluRay'] = torrents.br720
        if self.search_query.quality in ['all', '1080'] and torrents.br1080:
            available_torrents['1080p.BluRay'] = torrents.br1080
        if self.search_query.quality in ['all', '720'] and torrents.web720:
            available_torrents['720p.WEB'] = torrents.web720
        if self.search_query.quality in ['all', '1080'] and torrents.web1080:
            available_torrents['1080p.WEB'] = torrents.br1080
        return available_torrents

    MoviesList = List[Movie]

    def show_movies(self, movies: MoviesList):
        print('Movies List: ')
        for ind, movie in enumerate(movies):
            print('{0}{1}: {2} ({3}){4}'.format(
                Color.PURPLE, ind + 1, movie.name, movie.year, Color.END))
        while True:
            mid = int(input(Color.get_bold_string(Constants.movie_download_text)))
            if mid > len(movies) or mid < 1:
                Print.wrong_option()
                continue
            else:
                break
        movie_selected = movies[mid - 1]
        Print.bold_string(Constants.available_torrents_text)

        available_torrents = self.get_available_torrents(movie_selected.torrents)
        if len(available_torrents.values()) == 0:
            print('{0}{1}{2}'.format(Color.RED, Constants.no_torrent_text, Color.END))
        else:
            ati = 1
            for torrent_format in list(available_torrents):
                print('{0}{1}: {2}{3}'.format(Color.YELLOW, ati, torrent_format, Color.END))
                ati += 1
            if len(available_torrents) == 1:
                op = input('Press 1 to Download, Press any other key to exit\n')
                if op == '1':
                    torrent_link = list(available_torrents.values())[0]
                    Print.bold_string('{0}{1}{2}{3}'.format(
                        Constants.click_link_text, Color.RED, torrent_link, Color.END))
            else:
                Print.bold_string(Constants.movie_quality_text)
                qu = int(input())
                torrent_link = list(available_torrents.values())[qu - 1]
                Helper.open_magnet_link(torrent_link)
                Print.bold_string('{0}{1}{2}{3}'.format(
                    Constants.click_link_text, Color.RED, torrent_link, Color.END))
            Print.long_hash()
            if movie_selected.subtitle_url and movie_selected.subtitle_url != '':
                Print.bold_string(Constants.selection_text['subtitle'])
                download_subtitle = Helper.ask_for_options()
                if download_subtitle:
                    subtitle = Subtitle()
                    subtitle.search_subtitle(movie_selected.subtitle_url)
                Print.long_hash()
            print(Constants.another_movies_text.format(
                Color.RED, Color.get_bold_string(self.search_query.search_term)))
            reshow_movies = input(Color.get_yes_no())
            if reshow_movies == 'y' or reshow_movies == 'Y':
                self.show_movies(movies)

    def start(self, search_query: SearchQuery):
        url = search_query.get_url()
        crawler = Crawler(api_flag=self.api_flag)
        movies = crawler.crawl_list(url)
        if self.api_flag is True:
            return movies
        self.show_movies(movies)
        print(Constants.restart_search_text)
        restart_search = input('{0}\n'.format(Color.get_colored_yes()))
        if restart_search == 'y' or restart_search == 'Y':
            main()
        else:
            print('{0}{1}{2}'.format(Color.BLUE, Constants.thanks_text, Color.END))


class SearchInput:
    @staticmethod
    def create_query() -> SearchQuery:
        Print.long_hash()
        s = input(Color.get_bold_string(Constants.search_string_text))

        q = 'all'
        """
        print('Please enter any specific quality of your torrent: ')
        quality_options = Constants.quality
        for i in range(len(quality_options)):
            print('{0}: {1}'.format(i, quality_options[i]))
        q = int(input())
        while q > 4 or q < 0:
            print('Wrong option, Try again')
        q = quality_options[q]
        """
        g = Helper.take_optional_input('genre')
        o = Helper.take_optional_input('order')

        return SearchQuery(s, q, g, 0, o, 0, 'all')


def main():
    print('{0}###########################################'.format(Color.DARK_CYAN))
    print()
    print('#     #  ######  #       #  #  #####  #####')
    print('# # # #  #    #   #     #   #  #      #    ')
    print('#  #  #  #    #    #   #    #  ###    #####')
    print('#     #  #    #     # #     #  #          #')
    print('#     #  ######      #      #  #####  #####')
    print()
    print('###########################################')
    print('###                                    ####')
    print(' Welcome to torrent search and downloader ')
    print('###                                    ####')
    print('###########################################{0}'.format(Color.END))
    try:
        search_query = SearchInput.create_query()
        # search_query = SearchQuery('avengers', 'all', 'all', 0, 'latest', 0, 'all')
        search = Search(search_query)
        search.start(search_query)
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
