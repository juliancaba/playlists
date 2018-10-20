#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Webhook, db
import requests

bp_songs=Blueprint("bp_songs", __name__)


# OPERACIONES sobre songs
def delSong(id_song):
    aux = Song.query.filter_by(idSong=id_song)
    try:
        db.session.delete(aux.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":id_song}), 200)


def getSong(id_song):
    try:        
        aux = Song.query.filter_by(idSong=str(id_song))
        response = make_response(jsonify(aux.first().toJSON), 200)
    except:
        abort(404)
    return response


@bp_songs.route('/<path:id_song>', methods = ['DELETE','GET'])
def manager_song(id_song):
    if request.method == 'DELETE':
        return delSong(id_song)
    elif request.method == 'GET':
        return getSong(id_song)


def notify(idSong, genre):
    for itWH in Webhook.query.all():
        if genre and genre in itWH.genres:
            response=requests.post(itWH.idEndpoint, json = {'info':'new song in ' +url_for('bp_songs.manager_song', id_song=idSong, _external=True)})
            print(response.status_code)

    
def getSongs():
    listSongs = []
    for it in Song.query.all():
        listSongs.append(it.toJSON)
    return make_response(jsonify({"songs":listSongs}), 200)

                    
def addSong():
    attr = ['title', 'album', 'artist']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    title = request.json['title']
    album = request.json['album']
    artist = request.json['artist']
    genre = request.json.get('genre', None)
    idSong = (base64.b64encode((title + album + artist).encode())).decode('utf-8')
    newSong = Song(
        idSong=str(idSong),
        title=title,
        album=album,
        artist=artist,
        genre=genre,
        year=int(request.json.get('year',0)))
    try:
        db.session.add(newSong)
        db.session.commit()
    except:
        abort(409)
    notify(idSong, genre)
    return make_response (jsonify({"created":idSong}), 201)


@bp_songs.route('', methods = ['GET', 'POST'])
def manager_songs():
    if request.method == 'POST':
        return addSong()
    elif request.method == 'GET':
        return getSongs()
