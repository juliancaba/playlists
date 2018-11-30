#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import base64
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import songs

bp_songs=Blueprint("bp_songs", __name__)


# OPERACIONES sobre songs
def delSong(idSong):
    auxSong = list(filter(lambda t:t['id'] == idSong, songs))
    if len(auxSong) == 0:
        abort(404)
    songs.remove(auxSong[0])
    return make_response(jsonify({"deleted":idSong}), 200)


def getSong(idSong):
    auxSong = list(filter(lambda t:t['id'] == idSong, songs))
    if len(auxSong) == 0:
        abort(404)
    return make_response(jsonify(auxSong[0]), 200)


@bp_songs.route('/<path:idSong>', methods = ['DELETE','GET'])
def manager_song(idSong):
    if request.method == 'DELETE':
        return delSong(idSong)
    elif request.method == 'GET':
        return getSong(idSong)



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

