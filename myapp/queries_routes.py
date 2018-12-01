#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-


from google.appengine.ext import ndb
from flask import Blueprint, jsonify, abort, make_response, request

from myapp.models import Song, Album

bp_queries = Blueprint("bp_queries",__name__)

@bp_queries.route('/search')
def search():
    artist = request.args.get('artist',"", type=str)
    listQuery = Album.query(Album.artist==artist)
    return make_response(jsonify(Song.toJSONlist(listQuery)), 200)


@bp_queries.route('/searchGQL')
def searchGQL():
    artist = request.args.get('artist',"", type=str)
    listQuery = ndb.gql("SELECT * FROM Album WHERE artist='"+
                artist +"'")
    return make_response(jsonify(Song.toJSONlist(listQuery)), 200)


