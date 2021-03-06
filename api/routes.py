from flask import jsonify, request, Response
from api import app

from .data_helpers import get_all_games, get_all_platforms, get_game_by_id, get_edition_by_id, get_editions_by_platform_id, get_platform_by_id, get_searched_games, get_searched_editions, get_searched_platforms
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
def certain_platform_route(platform_id):
    print(platform_id)
    p = get_platform_by_id(platform_id)
    if p == None:
        return Response(response="404 Platform not found", status=404)
    p.editions = get_editions_by_platform_id(platform_id)
    return jsonify(p.jsonify())


@app.route('/platforms/<platform_id>/platform-editions')
def certain_platform_editions_route(platform_id):
    editions = get_editions_by_platform_id(platform_id)
    print(editions)
    edict = dictify_all(editions)
    return jsonify(edict)


@app.route('/platform-editions/<edition_id>')
def certain_edition_route(edition_id):
    e = get_edition_by_id(edition_id)
    print(e)
    if e == None:
        return Response(response="404 Edition not found", status=404)
    edict = dictify(e)
    return jsonify(edict)
    

@app.route('/platform-editions/search')
def search_editions_route():
    q = request.args.get('q')
    editions = get_searched_editions(q)
    dictified = dictify_all(editions)
    return jsonify(dictified)


@app.route('/games')
def all_games_route():
    games = get_all_games()
    dictified = dictify_all(games)
    return jsonify(dictified)


@app.route('/games/<game_id>')
def certain_game_route(game_id):
    g = get_game_by_id(game_id)
    print(g)
    if g == None:
        return Response(response="404 Game not found", status=404)
    gdict = dictify(g)
    return jsonify(gdict)


@app.route('/games/search')
def search_games_route():
    q = request.args.get('q')
    games = get_searched_games(q)
    dictified = dictify_all(games)
    return jsonify(dictified)
