#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Webhook, db
import requests

bp_songs=Blueprint("bp_songs", __name__)


# OPERACIONES sobre songs
def delSong(idSong):
    auxSong = Song.query.filter_by(idSong=idSong)
    try:
        db.session.delete(auxSong.first())
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idSong}), 200)


def getSong(idSong):
    try:        
        auxSong = Song.query.filter_by(idSong=str(idSong))
        response = make_response(jsonify(auxSong.first().toJSON), 200)
    except:
        abort(404)
    return response


@bp_songs.route('/<path:idSong>', methods = ['DELETE','GET'])
def manager_song(idSong):
    if request.method == 'DELETE':
        return delSong(idSong)
    elif request.method == 'GET':
        return getSong(idSong)


def notify(idSong, genre):
    for itWH in Webhook.query.all():
        if genre and genre in itWH.genres:
            response=requests.post(itWH.idEndpoint, json = {'info':'new song in ' +url_for('bp_songs.manager_song', idSong=idSong, _external=True)})
            print(response.status_code)

    
def getSongs():
    listSongs = []
    for itSong in Song.query.all():
        listSongs.append(itSong.toJSON)
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
