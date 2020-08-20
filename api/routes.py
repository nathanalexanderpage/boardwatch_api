from flask import jsonify, request, Response
from api import app

from .data_helpers import get_all_platforms, get_platform_by_id, get_searched_platforms
from .helpers import dictify, dictify_all


@app.route('/')
def index():
    return "you have reached Boardwatch API"


@app.route('/search')
def search():
    q = request.args.get('q')
    print(q)
    # perform smaller searches in each category for category-mixed search results
    return Response(response="501 Not Implemented", status=501)


@app.route('/platforms/search')
def search_platforms_route():
    q = request.args.get('q')
    platforms = get_searched_platforms(q)
    dictified = dictify_all(platforms)
    return jsonify(dictified)


@app.route('/platforms')
def all_platforms_route():
    platforms = get_all_platforms()
    dictified = dictify_all(platforms)
    return jsonify(dictified)


@app.route('/platforms/<platform_id>')
def platform_route(platform_id):
    p = get_platform_by_id(platform_id)
    print(p)
    if p == None:
        return Response(response="404 Platform not found", status=404)
    pdict = dictify(p)
    return jsonify(pdict)
    