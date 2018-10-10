#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import random
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Playlist, db
from myapp.songs_routes import bp_songs

bp_playlist=Blueprint("bp_playlist", __name__)


# OPERACIONES sobre playlists

@bp_playlist.route('/playlists', methods = ['GET'])
def getPlaylists():
    listPlaylists = []
    for it in Playlist.query.all():
        listPlaylists.append(it.toJSON)
    return make_response(jsonify({"playlists":listPlaylists}), 200)


def delPlaylist(id_ps):   
    auxPS = Playlist.query.filter_by(name=id_ps)
    try:
        db.session.delete(auxPS[0])
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":id_ps}), 200) 


def getPlaylist(id_ps):
    try:
        auxPS = Playlist.query.filter_by(name=id_ps)[0]
    except:
        abort(404)
    return make_response(jsonify(auxPS.toJSON), 200) 


def addPlaylist(id_ps):
    response = None
    auxPS = Playlist.query.filter_by(name=id_ps)
    
    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    try:
        auxPS.first().description = description
        response=make_response(jsonify({"updated":id_ps}), 200)
    except:        
        new_ps = Playlist(
            name = str(id_ps),
            description=description,
            songs_lst=[])
        try:
            db.session.add(new_ps)
            db.session.commit()
            response= make_response(jsonify({"id":id_ps}), 201)
        except:
            abort(409)
    return response


@bp_playlist.route('/playlists/<path:id_ps>', methods = ['DELETE', 'PUT', 'GET'])
def manager_playlist(id_ps):
    if request.method == 'GET':
        return getPlaylist(id_ps)
    elif request.method == 'PUT':
        return addPlaylist(id_ps)
    elif request.method == 'DELETE':
        return delPlaylist(id_ps)


@bp_playlist.route('/playlists/<id_ps>', methods = ['POST'])
@bp_playlist.route('/playlists/<id_ps>/songs', methods = ['POST'])
def addSongToAPlaylist(id_ps):
    if not request.json or not 'song' in request.json:
        abort(400)
    reqSong = request.json['song']

    try:
        auxSong = Song.query.filter_by(idSong=reqSong).first()
        auxPS = Playlist.query.filter_by(name=id_ps).first()
        if auxSong in auxPS.songs_lst:
            abort(409)
        auxPS.songs_lst.append(auxSong)
        db.session.commit()
    except:
        abort(404)
                
    return make_response(jsonify({"info":"Added "+ reqSong + " in " + id_ps + " playlist"}),200)


@bp_playlist.route('/playlists/<id_ps>/<id_song>', methods = ['DELETE'])
@bp_playlist.route('/playlists/<id_ps>/songs/<id_song>', methods = ['DELETE'])
def delSongOfAPlaylist(id_ps, id_song):
    try:
        auxPS = Playlist.query.filter_by(name=id_ps).first()
        auxSong = Song.query.filter_by(idSong=id_song).first()
        auxPS.songs_lst.remove(auxSong)
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"info":"Deleted "+ id_song + " from " + id_ps + " playlist"}),200)
    

