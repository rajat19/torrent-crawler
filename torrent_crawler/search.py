import signal
import traceback
from typing import Dict, List
from torrent_crawler.constants import Constants
from torrent_crawler.color import Color
from torrent_crawler.crawler import Crawler, Movie, Torrents
from torrent_crawler.helper import open_magnet_link, print_wrong_option, get_yes_no, print_long_hash
from torrent_crawler.subtitle import Subtitle


def sigint_handler(signum, frame):
    print('\n{0}{1}{2}'.format(Color.BLUE, Constants.thanks_text, Color.END))
    exit(1)


signal.signal(signal.SIGINT, sigint_handler)


class SearchQuery:
    def __init__(self, search_term, quality, genre, rating, order_by):
        self.search_term = search_term
        self.quality = quality
        self.genre = genre
        self.rating = rating
        self.order_by = order_by


class Search:
    def __init__(self, search_query: SearchQuery):
        self.search_query = search_query

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
                print_wrong_option()
                continue
            else:
                break
        movie_selected = movies[mid - 1]
        Color.print_bold_string(Constants.available_torrents_text)

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
                    Color.print_bold_string('{0}{1}{2}{3}'.format(
                        Constants.click_link_text, Color.RED, torrent_link, Color.END))
            else:
                Color.print_bold_string(Constants.movie_quality_text)
                qu = int(input())
                torrent_link = list(available_torrents.values())[qu - 1]
                open_magnet_link(torrent_link)
                Color.print_bold_string('{0}{1}{2}{3}'.format(
                    Constants.click_link_text, Color.RED, torrent_link, Color.END))
            print_long_hash()
            Color.print_bold_string(Constants.subtitles_selection_text)
            download_subtitle = input(get_yes_no())
            if download_subtitle == 'y' or download_subtitle == 'Y':
                subtitle = Subtitle()
                subtitle.search_subtitle(movie_selected.subtitle_url)

            print_long_hash()
            print(Constants.another_movies_text.format(
                Color.RED, Color.get_bold_string(self.search_query.search_term)))
            reshow_movies = input(get_yes_no())
            if reshow_movies == 'y' or reshow_movies == 'Y':
                self.show_movies(movies)

    def start(self, search_query: SearchQuery):
        url = Constants.search_url.format(search_query.search_term, search_query.quality, search_query.genre,
                                          search_query.rating, search_query.order_by)
        crawler = Crawler()
        movies = crawler.crawl_list(url)
        self.show_movies(movies)
        print(Constants.restart_search_text)
        restart_search = input('{0}\n'.format(Color.get_colored_yes()))
        if restart_search == 'y' or restart_search == 'Y':
            main()
        else:
            print('{0}{1}{2}'.format(Color.BLUE, Constants.thanks_text, Color.END))


class SearchInput:
    @staticmethod
    def take_genre_input() -> str:
        print_long_hash()
        Color.print_bold_string(Constants.genre_selection_text)
        genre_options = Constants.genre
        while True:
            want_genre = input(get_yes_no())
            if want_genre not in ['y', 'Y', 'n', 'N']:
                print_wrong_option()
                continue
            else:
                break
        g = 0
        if want_genre == 'y' or want_genre == 'Y':
            Color.print_bold_string(Constants.specific_genre_text)
            for i in range(1, len(genre_options)):
                print('{0}{1}: {2}{3}'.format(Color.YELLOW, i, genre_options[i], Color.END))
            while True:
                g = int(input())
                if 1 <= g <= 27:
                    break
                else:
                    print_wrong_option()
                    continue
            Color.print_colored_note(Constants.specific_genre_note.format(genre_options[g]))
        else:
            Color.print_colored_note(Constants.all_genre_note)
        return genre_options[g]

    @staticmethod
    def take_order_input() -> str:
        print_long_hash()
        Color.print_bold_string(Constants.order_selection_text)
        order_options = Constants.order_by
        while True:
            want_order = input(get_yes_no())
            if want_order not in ['y', 'Y', 'n', 'N']:
                print_wrong_option()
                continue
            else:
                break
        o = 0
        if want_order == 'y' or want_order == 'Y':
            Color.print_bold_string(Constants.specific_order_text)
            for i in range(1, len(order_options)):
                print('{0}{1}: {2}{3}'.format(Color.YELLOW, i, order_options[i], Color.END))
            while True:
                o = int(input())
                if o > 6 or o < 1:
                    print_wrong_option()
                    continue
                else:
                    break
            Color.print_colored_note(Constants.specific_order_note.format(order_options[0]))
        else:
            Color.print_colored_note(Constants.imdb_order_note)
        return order_options[o]

    def create_query(self) -> SearchQuery:
        print_long_hash()
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
        g = self.take_genre_input()
        o = self.take_order_input()

        return SearchQuery(s, q, g, 0, o)


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
        search_input = SearchInput()
        search_query = search_input.create_query()
        search = Search(search_query)
        search.start(search_query)
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
