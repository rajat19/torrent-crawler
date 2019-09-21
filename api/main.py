from flask import Flask, request, jsonify
from torrent_crawler.search import Search, SearchQuery
from torrent_crawler.constants import Constants
import json
from operator import attrgetter

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/movies', methods=['GET'])
def salvador():
    search_string = request.args.get('search')
    order_by = request.args.get('order') or Constants.order_by[0]
    genre = request.args.get('genre') or Constants.genre[0]
    quality = request.args.get('quality') or Constants.quality[0]
    rating = 0
    search_query = SearchQuery(search_string, quality, genre, rating, order_by)
    search = Search(search_query, True)
    movies = search.start(search_query)
    result = []
    for movie in movies:
        result.append(json.loads(movie.to_json()))
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
