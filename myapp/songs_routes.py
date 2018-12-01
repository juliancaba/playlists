#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from datetime import date, datetime
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Webhook, Album
import json, base64


bp_songs = Blueprint("bp_songs",__name__)


# OPERACIONES sobre songs

def delSong(urlsafeSong):
    try:
        keySong = ndb.Key(urlsafe=urlsafeSong)
    except:
        abort(404)
    keySong.delete()
    return make_response(jsonify({"deleted":urlsafeSong}), 200)


def getSong(urlsafeSong):
    try:
        keySong = ndb.Key(urlsafe=urlsafeSong)
    except:
        abort(404)
    auxSong = keySong.get()
    return make_response(jsonify(auxSong.toJSON), 200)


@bp_songs.route('/<path:urlsafeSong>', methods = ['DELETE','GET'])
def manager_song(urlsafeSong):
    if request.method == 'DELETE':
        return delSong(urlsafeSong)
    elif request.method == 'GET':
        return getSong(urlsafeSong)

    
def getSongs(idAlbum):
    listSongs = []
    if idAlbum == "":
        listSongs = Song.toJSONlist(Song.query())
    else:
        key = ndb.Key('Album', idAlbum)
        listQuery = Song.query(ancestor=key)
        listSongs = Song.toJSONlist(listQuery)
        
    return make_response(jsonify({"songs":listSongs}), 200)

                    
def addSong():
    attr = ['title', 'album']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    
    title = request.json['title']
    album = request.json['album']
    try:
        newSong = Song(
            parent=ndb.Key('Album', album),
            id=title)
    except:
        abort(404)
    keySong = newSong.put()
    
    return make_response (jsonify({"created":keySong.urlsafe()}), 201)


@bp_songs.route('', methods = ['GET', 'POST'])
def manager_songs():
    if request.method == 'POST':
        return addSong()
    elif request.method == 'GET':
        idAlbum = request.args.get('album',"", type=str)
        return getSongs(idAlbum)
