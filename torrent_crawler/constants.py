class Constants:
    # movie search constants
    quality = ['all', '720p', '1080p', '3D']
    genre = ['all', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
             'family', 'fantasy', 'film-noir', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery',
             'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'talk-show', 'thriller', 'war', 'western']
    order_by = ['rating', 'seeds', 'peers', 'year', 'likes', 'alphabetical', 'downloads']
    search_url = 'https://yts.am/browse-movies/{0}/{1}/{2}/{3}/{4}'

    # subtitle search constants
    subtitle_base_url = 'http://www.yifysubtitles.com/{0}'
    subtitle_search_url = 'http://www.yifysubtitles.com/search?q={0}'
    subtitle_movie_url = 'http://www.yifysubtitles.com/movie-imdb/{0}'

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
    subtitles_selection_text = 'Download subtitles for this movie'
    subtitle_language_text = 'Select language to get subtitles: '
    download_zip_text = 'Subtitle would be downloaded in {0}{1}. Please check there.'
    another_movies_text = 'Do you want to download another {0}{1} movie'

    # note
    specific_genre_note = 'Movies would be crawled for only {0} genre'
    all_genre_note = 'Movies would be crawled for all genre'
    specific_order_note = 'Movies would be downloaded by: {0}'
    imdb_order_note = 'Movies would be downloaded by IMDB rating'


if __name__ == '__main__':
    pass
