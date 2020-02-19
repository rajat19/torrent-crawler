from flask import Flask, request
from torrent_crawler.search import Search, SearchQuery
from torrent_crawler.constants import Constants
import json

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
    result = [json.loads(movie.to_json()) for movie in movies]
    count = len(result)
    if count == 0:
        message = 'No movies found'
    elif count == 1:
        message = 'Only 1 movie found'
    else:
        message = 'Total {count} movies found'.format(count=count)
    data = {
        'count': count,
        'message': message,
        'result': result
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
