#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import Flask, make_response, jsonify


# Por defecto el root es $PREFIX/var/myapp-instance
app=Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('../instance/development.cfg')

from myapp.songs_routes import bp_songs
from myapp.playlists_routes import bp_playlist
from myapp.webhook_routes import bp_webhook
from myapp.albums_routes import bp_album
from myapp.queries_routes import bp_queries

app.register_blueprint(bp_songs, url_prefix="/songs")
app.register_blueprint(bp_playlist)
app.register_blueprint(bp_webhook)
app.register_blueprint(bp_album)
app.register_blueprint(bp_queries)

# Este podría ir en otro Blueprint
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

