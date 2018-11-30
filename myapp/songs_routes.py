#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from datetime import date, datetime
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Song, Webhook
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
    return make_response(jsonify(auxSong.to_dict()), 200)


@bp_songs.route('/<path:urlsafeSong>', methods = ['DELETE','GET'])
def manager_song(urlsafeSong):
    if request.method == 'DELETE':
        return delSong(urlsafeSong)
    elif request.method == 'GET':
        return getSong(urlsafeSong)


def notify(urlsafeSong, genre):
    for itWH in Webhook.query():
        if genre and genre in itWH.genres:
            response=urlfetch.fetch(itWH.key.id(), payload = json.dumps({'info':'new song in ' +url_for('bp_songs.manager_song', urlsafeSong=urlsafeSong, _external=True)}), headers = {"Content-Type": "application/json"}, method=urlfetch.POST)
            print response.status_code

    
def getSongs():
    listSongs = []
    for itSongs in Song.query():
        listSongs.append(itSongs.to_dict())
    return make_response(jsonify({"songs":listSongs}), 200)

                    
def addSong():
    attr = ['title', 'album', 'artist']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    
    title = request.json['title']
    album = request.json['album']
    artist=request.json['artist']
    strYear = request.json.get('year',"1900-01-01")
    year=datetime.strptime(strYear, "%Y-%m-%d")
    genre=request.json.get('genre',"")
    newSong = Song(
        id = base64.b64encode(title + album + artist),
        title=title,
        album=album,
        artist=request.json.get('artist',""),
        genre=genre,
        year=year)
    keySong = newSong.put()
    notify(keySong.urlsafe(), genre)
    return make_response (jsonify({"created":keySong.urlsafe()}), 201)


@bp_songs.route('', methods = ['GET', 'POST'])
def manager_songs():
    if request.method == 'POST':
        return addSong()
    elif request.method == 'GET':
        return getSongs()
