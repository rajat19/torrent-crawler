from crawler import Crawler


class Constants:
    quality = ['all', '720p', '1080p', '3D']
    genre = ['all', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
             'family', 'fantasy', 'film-noir', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery',
             'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'talk-show', 'thriller', 'war', 'western']
    order_by = ['seeds', 'peers', 'year', 'rating', 'likes', 'alphabetical', 'downloads']


class SearchQuery:
    def __init__(self, search_term, quality, genre, rating, order_by):
        self.search_term = search_term
        self.quality = quality
        self.genre = genre
        self.rating = rating
        self.order_by = order_by


class Search:
    search_url = 'https://yts.am/browse-movies/{0}/{1}/{2}/{3}/{4}'

    def search_torrent(self, search_query: SearchQuery):
        url = self.search_url.format(search_query.search_term, search_query.quality, search_query.genre,
                                     search_query.rating, search_query.order_by)
        crawler = Crawler()
        movies = crawler.crawl_list(url)
        print('Movies List: ')
        for ind, movie in enumerate(movies):
            print('{0}: {1} ({2})'.format(ind+1, movie['name'], movie['year']))
        print('Enter movie to download: ')
        mid = int(input())
        while mid > len(movies) or mid < 1:
            print('Wrong input, Try again')
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
            ati = 0
            for torrent_format in available_torrents:
                print('{0}: {1}'.format(ati, torrent_format))
                ati += 1
            if len(available_torrents) == 1:
                print('Press 1 to Download, Press any other key to exit')
                op = input()
                if op == '1':
                    tlink = list(available_torrents.values())[0]
                    print('Click this link: {}'.format(tlink))
            else:
                print('Enter quality to download:')
                qu = int(input())
                tlink = list(available_torrents.values())[qu-1]
                print('Click this link: {}'.format(tlink))


if __name__ == '__main__':
    try:
        print('Welcome to torrent search and downloader')
        print('Please enter search string: ')
        s = input()

        q = 0
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

        print('Please enter any specific genre of your torrent: ')
        genre_options = Constants.genre
        for i in range(len(genre_options)):
            print('{0}: {1}'.format(i, genre_options[i]))
        g = int(input())
        while g > 27 or g < 0:
            print('Wrong option, Try again')
        g = genre_options[g]

        print('Order by which movies would be sorted: ')
        order_options = Constants.order_by
        for i in range(len(order_options)):
            print('{0}: {1}'.format(i+1, order_options[i]))
        o = int(input())
        while o > 9 or o < 1:
            print('Wrong option, Try again')
        o = order_options[o-1]

        sq = SearchQuery(s, q, g, 0, o)
        search = Search()
        search.search_torrent(sq)
    except Exception as e:
        print(e)
