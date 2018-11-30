#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


from datetime import date, datetime
from google.appengine.ext import ndb
from flask import Blueprint, jsonify, abort, make_response, request

from myapp.models import Song, Playlist
from myapp.songs_routes import bp_songs

bp_playlist = Blueprint("bp_playlist",__name__)


# OPERACIONES sobre playlists

@bp_playlist.route('/playlists', methods = ['GET'])
def getPlaylists():
    listPlaylists = []
    for it in Playlist.query():
        listPlaylists.append(it.toJSON)
    return make_response(jsonify({"playlists":listPlaylists}), 200)


def delPlaylist(idPlaylist):   
    try:
        keyPlaylist = ndb.Key('Playlist',idPlaylist)
    except:
        abort(404)
    keyPlaylist.delete()
    return make_response(jsonify({"deleted":keyPlaylist.id}), 200) 


def getPlaylist(idPlaylist):
    try:
        keyPlaylist = ndb.Key('Playlist',idPlaylist)
    except:
        abort(404)
    return make_response(jsonify((keyPlaylist.get()).to_dict()), 200) 


def addPlaylist(idPlaylist):
    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    
    try:
        # If Playlist exits, it will be updated completly
        keyPlaylist = ndb.Key('Playlist',idPlaylist)
        auxPlaylist = keyPlaylist.get()
        auxPlaylist.songs=[]
        auxPlaylist.description = description
        keyPlaylist_i = auxPlaylist.put()
        response = make_response(jsonify({"updated":keyPlaylist_i.id()}), 200)
    except:        
        newPlaylist = Playlist(
            id = idPlaylist,
            description=description,
            songs=[])
        try:
            keyPlaylist_i = newPlaylist.put()
            response = make_response(jsonify({"created":keyPlaylist_i}), 201)
        except:
            abort(409)
    '''auxPlaylist = getPlaylistKey(id_ps).get()
    try:
        auxPlaylist.description = description
        auxPlaylist.put()
    except:        
        new_ps = Playlist(
            id = id_ps,
            description=description,
            songs=[])
        try:
            idPlaylist = new_ps.put()
            response= make_response(jsonify({"id":idPlaylist}), 201)
        except:
            abort(409)'''
    return response


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

    try:
        keySong = ndb.Key(urlsafe=idSong)
        keyPlaylist = ndb.Key('Playlist',idPlaylist)
    except:
        abort(404)

    auxPlaylist = keyPlaylist.get()
 
    if keySong.urlsafe() in auxPlaylist.songs:
        abort(409)

    auxPlaylist.songs.append(keySong.urlsafe())
    keyPlaylist_i = auxPlaylist.put()        
    return make_response(("Added "+ idSong + " in " + keyPlaylist_i.id() + " playlist"), 200)


@bp_playlist.route('/playlists/<idPlaylist>/<idSong>', methods = ['DELETE'])
@bp_playlist.route('/playlists/<idPlaylist>/songs/<idSong>', methods = ['DELETE'])
def delSongOfAPlaylist(idPlaylist, idSong):
    try:
        keyPlaylist = ndb.Key('Playlist',idPlaylist)
        auxPlaylist = keyPlaylist.get()
        auxPlaylist.songs.remove(idSong)
        keyPlaylist_i = auxPlaylist.put()
    except:
        abort(404)
    return make_response(("Deleted "+ idSong + " from " + keyPlaylist_i.id() + " playlist"), 200)
    

