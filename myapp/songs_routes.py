#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import songs

bp_songs=Blueprint("bp_songs", __name__)


# OPERACIONES sobre songs
def delSong(id_song):
    aux = list(filter(lambda t:t['id'] == id_song, songs))
    if len(aux) == 0:
        abort(404)
    songs.remove(aux[0])
    return make_response(jsonify({"deleted":id_song}), 200)


def getSong(id_song):
    aux = list(filter(lambda t:t['id'] == id_song, songs))
    if len(aux) == 0:
        abort(404)
    return make_response(jsonify({"song":aux[0]}), 200)


@bp_songs.route('/<path:id_song>', methods = ['DELETE','GET'])
def manager_song(id_song):
    if request.method == 'DELETE':
        return delSong(id_song)
    elif request.method == 'GET':
        return getSong(id_song)



def getSongs():
    return make_response(jsonify({"songs":songs}), 200)

                    
def addSong():
    attr = ['title', 'album', 'artist']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    title = request.json['title']
    album = request.json['album']
    artist = request.json['artist']
    idSong = (base64.b64encode((title + album + artist).encode())).decode('utf-8')
    print (idSong)
    if len(list(filter(lambda t:t['id']==idSong,songs))) != 0:
        abort(409)
    newSong = {
        'id':idSong,
        'title':title,
        'album':album,
        'artist':artist,
        'year':request.json.get('year',"")}
    songs.append(newSong)
    return make_response (jsonify({"created":str(idSong)}), 201)


@bp_songs.route('', methods = ['GET', 'POST'])
def manager_songs():
    if request.method == 'POST':
        return addSong()
    elif request.method == 'GET':
        return getSongs()

