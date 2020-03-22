import json
import os
from torrent_crawler.constants import Constants


class Ratings:
    def __init__(self, ratings):
        self.rotten_tomatoes_critics, self.rotten_tomatoes_audience, self.imdb = ['']*3
        if Constants.rotten_tomatoes_critics_rating in ratings:
            self.rotten_tomatoes_critics = ratings[Constants.rotten_tomatoes_critics_rating]
        if Constants.rotten_tomatoes_audience_rating in ratings:
            self.rotten_tomatoes_audience = ratings[Constants.rotten_tomatoes_audience_rating]
        if Constants.imdb_rating in ratings:
            self.imdb = ratings[Constants.imdb_rating]


class Torrents:
    def __init__(self, torrents):
        self.br3d = torrents[Constants.blu_ray_3d] if Constants.blu_ray_3d in torrents else None
        self.br1080 = torrents[Constants.blu_ray_1080p] if Constants.blu_ray_1080p in torrents else None
        self.br720 = torrents[Constants.blu_ray_720p] if Constants.blu_ray_720p in torrents else None
        self.web1080 = torrents[Constants.web_1080p] if Constants.web_1080p in torrents else None
        self.web720 = torrents[Constants.web_720p] if Constants.web_720p in torrents else None


class Movie:
    header_format = 'ID|Name|Year|Link|Rotten Tomatoes Critics|Rotten Tomatoes Audience|IMDb' \
                    '|3D.BluRay|720p.BluRay|1080p.BluRay|720p.WEB|1080p.WEB\n' \
                    '---|---|---|---|---|---|---|---|---|---|---|---'
    file_name = 'movies.md'
    movie_format = '{}|{}|{}|[Link]({})|{}|{}|{}|' \
                   ' [3D.BluRay]({})|[720p.BluRay]({})|[1080p.BluRay]({})|[720p.WEB]({})|[1080p.WEB]({})'
    readme_created = True

    def __init__(self, movie_id, name, link, year):
        self.id = movie_id
        self.name = name
        self.link = link
        self.year = year
        self.torrents = None
        self.ratings = None
        self.subtitle_url = ''

    def set_torrents(self, torrent_list):
        self.torrents = Torrents(torrent_list)

    def set_ratings(self, ratings):
        self.ratings = Ratings(ratings)

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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
