from torrent_crawler.crawler import Crawler


class Constants:
    quality = ['all', '720p', '1080p', '3D']
    genre = ['all', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
             'family', 'fantasy', 'film-noir', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery',
             'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'talk-show', 'thriller', 'war', 'western']
    order_by = ['rating', 'seeds', 'peers', 'year', 'likes', 'alphabetical', 'downloads']
    search_url = 'https://yts.am/browse-movies/{0}/{1}/{2}/{3}/{4}'

class SearchQuery:
    def __init__(self, search_term, quality, genre, rating, order_by):
        self.search_term = search_term
        self.quality = quality
        self.genre = genre
        self.rating = rating
        self.order_by = order_by


class Search:

    def search_torrent(self, search_query: SearchQuery):
        url = Constants.search_url.format(search_query.search_term, search_query.quality, search_query.genre,
                                          search_query.rating, search_query.order_by)
        crawler = Crawler()
        movies = crawler.crawl_list(url)
        print('Movies List: ')
        for ind, movie in enumerate(movies):
            print('{0}: {1} ({2})'.format(ind+1, movie['name'], movie['year']))
        while True:
            mid = int(input('Enter movie to download: '))
            if mid > len(movies) or mid < 1:
                print('Wrong input, Try again')
                continue
            else:
                break
        movie_selected = movies[mid - 1]
        print('Available torrents: ')
        available_torrents = {}
        if search_query.quality == 'all':
            available_torrents = movie_selected['torrents']
        elif search_query.quality == '3D' and '3D' in movie_selected['torrents']:
            available_torrents = {'3D': movie_selected['torrents']['3D']}
        elif search_query.quality == '720p' and '720p.BluRay' in movie_selected['torrents']:
            available_torrents = {'720p': movie_selected['torrents']['720p.BluRay']}
        elif search_query.quality == '1080p' and '1080p.BluRay' in movie_selected['torrents']:
            available_torrents = {'720p': movie_selected['torrents']['1080p.BluRay']}
        elif search_query.quality == '720p' and '720p.WEB' in movie_selected['torrents']:
            available_torrents = {'720p': movie_selected['torrents']['720p.WEB']}
        elif search_query.quality == '1080p' and '1080p.WEB' in movie_selected['torrents']:
            available_torrents = {'720p': movie_selected['torrents']['1080p.WEB']}

        if len(available_torrents.values()) == 0:
            print('No torrents available for this movie')
        else:
            ati = 1
            for torrent_format in available_torrents:
                print('{0}: {1}'.format(ati, torrent_format))
                ati += 1
            if len(available_torrents) == 1:
                op = input('Press 1 to Download, Press any other key to exit\n')
                if op == '1':
                    tlink = list(available_torrents.values())[0]
                    print('Click this link: {}'.format(tlink))
            else:
                print('Enter movie quality to download:')
                qu = int(input())
                tlink = list(available_torrents.values())[qu-1]
                print('Click this link: {}'.format(tlink))
        print('################################')
        restart_search = input('Do you want to start searching again\ny: Yes\n')
        if restart_search == 'y' or restart_search == 'Y':
            self.take_input()

    @staticmethod
    def take_genre_input():
        print('########################################')
        print('Do you want to search some specific genre: ')
        genre_options = Constants.genre
        while True:
            want_genre = input('y: Yes\nn: No\n')
            if want_genre not in ['y', 'Y', 'n', 'N']:
                print('Wrong option, Try again')
                continue
            else:
                break
        g = 0
        if want_genre == 'y' or want_genre == 'Y':
            print('Please enter any specific genre of your torrent: ')
            for i in range(1, len(genre_options)):
                print('{0}: {1}'.format(i, genre_options[i]))
            while True:
                g = int(input())
                if 1 <= g <= 27:
                    print('Wrong option, Try again')
                    continue
                else:
                    break
            print('Note:: Movies would be crawled for only {0} genre'.format(genre_options[g]))
        else:
            print('Note:: Movies would be crawled for all genre')
        return genre_options[g]

    @staticmethod
    def take_order_input():
        print('########################################')
        print('Do you want any specific order by which movies should be sorted')
        order_options = Constants.order_by
        while True:
            want_order = input('y: Yes\nn: No\n')
            if want_order not in ['y', 'Y', 'n', 'N']:
                print('Wrong option, Try again')
                continue
            else:
                break
        o = 0
        if want_order == 'y' or want_order == 'Y':
            print('Order by which movies would be sorted: ')
            for i in range(1, len(order_options)):
                print('{0}: {1}'.format(i, order_options[i]))
            while True:
                o = int(input())
                if o > 6 or o < 1:
                    print('Wrong option, Try again')
                    continue
                else:
                    break
            print('Note:: Movies would be downloaded by: {}'.format(order_options[o]))
        else:
            print('Note:: Movies would be downloaded by IMDB rating')
        return order_options[o]

    def take_input(self):
        try:
            print('##########################################')
            s = input('Please enter search string: ')

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

            sq = SearchQuery(s, q, g, 0, o)
            self.search_torrent(sq)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print('##########################################')
    print()
    print('#     #  #####  #   #  #  #####  #####')
    print('# # # #  #   #  #   #  #  #      #    ')
    print('#  #  #  #   #  #   #  #  ###    #####')
    print('#     #  #   #   # #   #  #          #')
    print('#     #  #####    #    #  #####  #####')
    print()
    print('##########################################')
    print('###                                    ###')
    print(' Welcome to torrent search and downloader ')
    print('###                                    ###')
    print('##########################################')
    search = Search()
    search.take_input()
