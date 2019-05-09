class Constants:
    # movie search constants
    quality = ['all', '720p', '1080p', '3D']
    genre = ['all', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
             'family', 'fantasy', 'film-noir', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery',
             'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'talk-show', 'thriller', 'war', 'western']
    order_by = ['rating', 'seeds', 'peers', 'year', 'likes', 'alphabetical', 'downloads']
    search_url = 'https://yts.am/browse-movies/{0}/{1}/{2}/{3}/{4}'

    # texts
    search_string_text = 'Please enter search string: '
    genre_selection_text = 'Do you want to search some specific genre: '
    wrong_option_text = 'Wrong option, Try again'
    specific_genre_text = 'Please enter any specific genre of your torrent: '
    order_selection_text = 'Do you want any specific order by which movies should be sorted'
    specific_order_text = 'Select order by which movies should be sorted: '
    movie_download_text = 'Enter movie to download: '
    available_torrents_text = 'Available torrents: '
    no_torrent_text = 'No torrents yet available for this movie'
    movie_quality_text = 'Enter movie quality to download:'
    click_link_text = 'Torrent link will open automatically, If not then Click this link: '
    restart_search_text = 'Do you want to start searching again'
    thanks_text = 'Thanks for using torrent-search . Keep Seeding'

    # note
    specific_genre_note = 'Movies would be crawled for only {0} genre'
    all_genre_note = 'Movies would be crawled for all genre'
    specific_order_note = 'Movies would be downloaded by: {0}'
    imdb_order_note = 'Movies would be downloaded by IMDB rating'


if __name__ == '__main__':
    pass
