from flask import jsonify, Response
from api import app

from .data_helpers import get_all_platforms, get_platform_by_id
from .helpers import dictify, dictify_all


@app.route('/')
def index():
    return "you have reached Boardwatch API"


@app.route('/platforms')
def all_platforms():
    platforms = get_all_platforms()
    dicified = dictify_all(platforms)
    return jsonify(dicified)

@app.route('/platforms/<platform_id>')
def platform(platform_id):
    p = get_platform_by_id(platform_id)
    print(p)
    if p == None:
        return Response(response="404 Not Found", status=404)
    pdict = dictify(p)
    return jsonify(pdict)
    