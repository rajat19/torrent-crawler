class Constants:
    # movie search constants
    input_types = ['genre', 'order', 'subtitle']
    options = {
        'quality': ['all', '720p', '1080p', '3D'],
        'genre': ['all', 'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'documentary', 'drama',
                  'family', 'fantasy', 'film-noir', 'game-show', 'history', 'horror', 'music', 'musical', 'mystery',
                  'news', 'reality-tv', 'romance', 'sci-fi', 'sport', 'talk-show', 'thriller', 'war', 'western'],
        'order': ['rating', 'seeds', 'peers', 'year', 'likes', 'alphabetical', 'downloads']
    }
    search_url = 'https://yts.mx/browse-movies/{0}/{1}/{2}/{3}/{4}/{5}/{6}'

    # yts constants
    rotten_tomatoes_critics_rating = 'Rotten Tomatoes Critics - Certified Fresh'
    rotten_tomatoes_audience_rating = 'Rotten Tomatoes Audience - Upright'
    imdb_rating = 'IMDb Rating'
    blu_ray_3d = '3D.BluRay'
    blu_ray_1080p = '1080p.BluRay'
    blu_ray_720p = '720p.BluRay'
    web_1080p = '1080p.WEB'
    web_720p = '720p.WEB'

    # subtitle search constants
    subtitle_base_url = 'http://www.yifysubtitles.org/{0}'
    subtitle_search_url = 'http://www.yifysubtitles.org/search?q={0}'
    subtitle_movie_url = 'http://www.yifysubtitles.org/movie-imdb/{0}'

    # texts
    search_string_text = 'Please enter search string: '
    selection_text = {
        'genre': 'Do you want to search some specific genre: ',
        'order': 'Do you want any specific order by which movies should be sorted',
        'subtitle': 'Download subtitles for this movie'
    }
    specific_text = {
        'genre': 'Please enter any specific genre of your torrent: ',
        'order': 'Select order by which movies should be sorted: ',
        'subtitle': 'Select language to get subtitles: ',
    }
    specific_final_option = {
        'genre': 'Movies would be crawled for only {0} genre',
        'order': 'Movies would be downloaded by: {0}',
    }
    special_final_option = {
        'genre': 'Movies would be crawled for all genre',
        'order': 'Movies would be downloaded by IMDB rating'
    }
    wrong_option_text = 'Wrong option, Try again'
    movie_download_text = 'Enter movie to download: '
    available_torrents_text = 'Available torrents: '
    no_torrent_text = 'No torrents yet available for this movie'
    movie_quality_text = 'Enter movie quality to download:'
    click_link_text = 'Torrent link will open automatically, If not then Click this link: '
    restart_search_text = 'Do you want to start searching again'
    thanks_text = 'Thanks for using torrent-search . Keep Seeding'
    download_zip_text = 'Subtitle would be downloaded in {0}{1}. Please check there.'
    another_movies_text = 'Do you want to download another {0}{1} movie'


if __name__ == '__main__':
    pass
