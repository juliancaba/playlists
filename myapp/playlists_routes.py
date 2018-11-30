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


def delPlaylist(idPlaylist):    
    auxPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))
    if len(auxPlaylist) == 0:
        abort(404)
    playlists.remove(auxPlaylist[0])
    return make_response(jsonify({'deleted':auxPlaylist[0]['name']}), 200)


def getPlaylist(idPlaylist):    
    auxPlaylist = list(filter(lambda t:t['name'] == str(idPlaylist), playlists))
    if len(auxPlaylist) == 0:
        abort(404)
    return make_response(jsonify(auxPlaylist[0]), 200)


def addPlaylist(idPlaylist):
    auxPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))

    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    if len(auxPlaylist) != 0:
        auxPlaylist[0]['description'] = description
        auxPlaylist[0]['songs'] = []
        return make_response(jsonify({"updated":str(idPlaylist)}), 200)
        
    newPlaylist = {
        'name' : idPlaylist,
        'description':description,
        'songs':[]}
    playlists.append(newPlaylist)
    return make_response(jsonify({"created":str(idPlaylist)}), 201)


@bp_playlist.route('/playlists/<path:idPlaylist>', methods = ['DELETE', 'PUT', 'GET'])
def manager_playlist(idPlaylist):
    if request.method == 'GET':
        return getPlaylist(idPlaylist)
    elif request.method == 'PUT':
        return addPlaylist(idPlaylist)
    elif request.method == 'DELETE':
        return delPlaylist(idPlaylist)


@bp_playlist.route('/playlists/<idPlaylist>', methods = ['POST'])
@bp_playlist.route('/playlists/<idPlaylist>/songs', methods = ['POST'])
def addSongToAPlaylist(idPlaylist):
    if not request.json or not 'song' in request.json:
        abort(400)
    idSong = request.json['song']
    listPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))
    if len(listPlaylist) == 0:
        abort(404)
    listSong = list(filter(lambda t:t['id'] == idSong, songs))
    if len(listSong) == 0:
        abort(404)
    hateoasSong = url_for('bp_songs.manager_song', idSong=idSong, _external=True)
    if hateoasSong in listPlaylist[0]['songs']:
        abort(409)
        
    listPlaylist[0]['songs'].append(hateoasSong)
        
    return make_response(("Added "+ idSong + " in " + idPlaylist + " playlist"), 200)


@bp_playlist.route('/playlists/<idPlaylist>/<idSong>', methods = ['DELETE'])
@bp_playlist.route('/playlists/<idPlaylist>/songs/<idSong>', methods = ['DELETE'])
def delSongOfAPlaylist(idPlaylist, idSong):
    listPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))
    if len(listPlaylist) == 0:
        abort(404)

    listSongsPlaylist = listPlaylist[0]['songs']
    hateoasSong = url_for('bp_songs.manager_song', idSong=idSong, _external=True)
    
    listSongs = list(filter(lambda t:t == hateoasSong, listSongsPlaylist))
    if len(listSongs) == 0:
        abort(404)
        
    listPlaylist[0]['songs'].remove(listSongs[0])
        
    return make_response(("Deleted "+ idSong + " from " + idPlaylist + " playlist"), 200)
    
