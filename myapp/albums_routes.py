#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-


from datetime import date, datetime
from google.appengine.ext import ndb
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from google.appengine.api import urlfetch

import json

from myapp.models import Song, Album, Webhook


bp_album = Blueprint("bp_album",__name__)



def notify(urlsafeAlbum, genre):
    for itWebhook in Webhook.query():
        if genre and genre in itWebhook.genres:
            response=urlfetch.fetch(itWebhook.key.id(),
                                      payload = json.dumps({'info':'new album in ' +url_for('bp_album.getAlbum', urlsafeAlbum=urlsafeAlbum, _external=True)}),
                                      headers = {"Content-Type": "application/json"},
                                      method=urlfetch.POST)
            print response.status_code


@bp_album.route('/albums', methods = ['POST'])
def addAlbum():
    if not request.json or not 'title' in request.json:
        abort(400)
    title = request.json['title']
    strYear = request.json.get('year',"1900-01-01")
    year = datetime.strptime(strYear,"%Y-%m-%d")
    genre = request.json.get('genre',None)
    newAlbum = Album(
        id=title,
        artist=request.json.get('artist',"anonymous"),
        genre=genre,
        year=year)
        
    keyAlbum=newAlbum.put()
    notify(keyAlbum.urlsafe(), genre)
    return make_response (jsonify({"created":keyAlbum.urlsafe()}), 201)
    

    

@bp_album.route('/albums/<urlsafeAlbum>', methods = ['GET', 'DELETE'])
def getAlbum(urlsafeAlbum):
    try:
        keyAlbum=ndb.Key(urlsafe=urlsafeAlbum)
        auxAlbum = keyAlbum.get()
        if request.method == 'DELETE':
            try:
                songList = Song.query(ancestor=keyAlbum)
                songKeys = [it.key for it in songList]
                ndb.delete_multi(songKeys)
                keyAlbum.delete()
                return make_response (jsonify({'deleted':keyAlbum.id()}), 200)
            except:
                abort(404)                
    except:
        abort(404)
    return make_response (jsonify(auxAlbum.toJSON), 200)
    
