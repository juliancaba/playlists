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
    for itPlaylist in Playlist.query.all():
        listPlaylists.append(itPlaylist.toJSON)
    return make_response(jsonify({"playlists":listPlaylists}), 200)


def delPlaylist(idPlaylist):   
    auxPlaylist = Playlist.query.filter_by(name=idPlaylist)
    try:
        db.session.delete(auxPlaylist[0])
        db.session.commit()
    except:
        abort(404)
    return make_response(jsonify({"deleted":idPlaylist}), 200) 


def getPlaylist(idPlaylist):
    try:
        auxPlaylist = Playlist.query.filter_by(name=idPlaylist)[0]
    except:
        abort(404)
    return make_response(jsonify(auxPlaylist.toJSON), 200) 


def addPlaylist(idPlaylist):
    response = None
    auxPlaylist = Playlist.query.filter_by(name=idPlaylist)
    
    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    try:
        auxPlaylist.first().description = description
        auxPlaylist.first().songs_lst = []
        response=make_response(jsonify({"updated":idPlaylist}), 200)
    except:        
        newPlaylist = Playlist(
            name = str(idPlaylist),
            description=description,
            songs_lst=[])
        try:
            db.session.add(newPlaylist)
            db.session.commit()
            response= make_response(jsonify({"created":idPlaylist}), 201)
        except:
            abort(409)
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
        auxSong = Song.query.filter_by(idSong=idSong).first()
        auxPlaylist = Playlist.query.filter_by(name=idPlaylist).first()
        if auxSong in auxPlaylist.songs_lst:
            abort(409)
        auxPlaylist.songs_lst.append(auxSong)
        db.session.commit()
    except:
        abort(404)
                
    return make_response(("Added "+ idSong + " in " + idPlaylist + " playlist"), 200)


@bp_playlist.route('/playlists/<idPlaylist>/<idSong>', methods = ['DELETE'])
@bp_playlist.route('/playlists/<idPlaylist>/songs/<idSong>', methods = ['DELETE'])
def delSongOfAPlaylist(idPlaylist, idSong):
    try:
        auxPlaylist = Playlist.query.filter_by(name=idPlaylist).first()
        auxSong = Song.query.filter_by(idSong=idSong).first()
        auxPlaylist.songs_lst.remove(auxSong)
        db.session.commit()
    except:
        abort(404)
    return make_response(("Deleted "+ idSong + " from " + idPlaylist + " playlist"), 200)
    

