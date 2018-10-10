#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import random
import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import playlists, songs
from myapp.songs_routes import bp_songs

bp_playlist=Blueprint("bp_playlist", __name__)


# OPERACIONES sobre playlists
@bp_playlist.route('/playlists', methods = ['GET'])
def getPlaylists():
    return make_response(jsonify({"playlists":playlists}), 200)


def delPlaylist(id_ps):    
    aux = list(filter(lambda t:t['name'] == id_ps, playlists))
    if len(aux) == 0:
        abort(404)
    playlists.remove(aux[0])
    return make_response(jsonify({'deleted':aux[0]['name']}), 200)


def getPlaylist(id_ps):    
    aux = list(filter(lambda t:t['name'] == str(id_ps), playlists))
    if len(aux) == 0:
        abort(404)
    return make_response(jsonify(aux[0]), 200)


def addPlaylist(id_ps):
    aux = list(filter(lambda t:t['name'] == id_ps, playlists))

    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    if len(aux) != 0:
        aux[0]['description'] = description
        return make_response(jsonify({"updated":str(id_ps)}), 200)
        
    new_ps = {
        'name' : id_ps,
        'description':description,
        'songs':[]}
    playlists.append(new_ps)
    return make_response(jsonify({"id":str(id_ps)}), 201)


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
    lstPS = list(filter(lambda t:t['name'] == id_ps, playlists))
    if len(lstPS) == 0:
        abort(404)
    lstSong = list(filter(lambda t:t['id'] == reqSong, songs))
    if len(lstSong) == 0:
        abort(404)
    hateoasSong = url_for('bp_songs.manager_song', id_song=reqSong, _external=True)
    if hateoasSong in lstPS[0]['songs']:
        abort(409)
        
    lstPS[0]['songs'].append(hateoasSong)
        
    return jsonify({"info":"Added "+ reqSong + " in " + id_ps + " playlist"})


@bp_playlist.route('/playlists/<id_ps>/<id_song>', methods = ['DELETE'])
@bp_playlist.route('/playlists/<id_ps>/songs/<id_song>', methods = ['DELETE'])
def delSongOfAPlaylist(id_ps, id_song):
    auxPS = list(filter(lambda t:t['name'] == id_ps, playlists))
    if len(auxPS) == 0:
        abort(404)

    psSongs = auxPS[0]['songs']
    hateoasSong = url_for('bp_songs.manager_song', id_song=id_song, _external=True)
    
    auxS = list(filter(lambda t:t == hateoasSong, psSongs))
    if len(auxS) == 0:
        abort(404)
        
    auxPS[0]['songs'].remove(auxS[0])
        
    return jsonify({"info":"Deleted "+ id_song + " from " + id_ps + " playlist"})
    
