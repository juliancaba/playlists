#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy


# Por defecto el root es $PREFIX/var/myapp-instance
app=Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('../instance/development.cfg')

db = SQLAlchemy(app)



from myapp.songs_routes import bp_songs
from myapp.playlists_routes import bp_playlist
from myapp.webhook_routes import bp_webhook

app.register_blueprint(bp_songs, url_prefix="/songs")
app.register_blueprint(bp_playlist)
app.register_blueprint(bp_webhook)


db.init_app(app)
with app.app_context():
    db.create_all()

# Este podría ir en otro Blueprint
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

