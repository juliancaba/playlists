#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import url_for
from google.appengine.ext import ndb

class Song(ndb.Model):
    title = ndb.StringProperty(required=True)
    artist = ndb.StringProperty()
    album = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=False)
    year = ndb.DateProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
        
    @classmethod
    def getAll(self):
        auxSongsList = []
        for itSongs in Song.query():
            auxSongsList.append(itSongs.to_dict())
        return auxSongsList

    
class Playlist(ndb.Model):
    description = ndb.StringProperty()
    songs = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @property
    def toJSON(self):
        from songs_routes import bp_songs
        aux = self.to_dict()
        aux_lst = []
        for it in self.songs:
            aux_lst.append(url_for('bp_songs.manager_song', urlsafeSong=it, _external=True))
        aux['songs']=aux_lst
        return aux

    
class Webhook(ndb.Model):
    #idEndpoint = ndb.StringProperty(required=True)
    genres = ndb.StringProperty(repeated=True)
    
    @classmethod
    def getAll(self):
        auxHooks = []
        for itHook in Webhook.query():
            auxHooks.append(itHook.to_dict())
        return auxHooks
