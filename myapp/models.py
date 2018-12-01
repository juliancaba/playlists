#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import url_for
from google.appengine.ext import ndb


class Album(ndb.Model):
    #title = ndb.StringProperty()    
    artist = ndb.StringProperty()
    year = ndb.DateProperty(required=False)
    genre = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    
    @property
    def toJSON(self):
        from songs_routes import bp_songs
        aux = self.to_dict()
        aux_lst = []
        songList = Song.query(ancestor=self.key)
        for it in songList:
            aux_lst.append(url_for('bp_songs.manager_song', urlsafeSong=it.key.urlsafe(), _external=True))
        aux['songs']=aux_lst
        return aux

    
class Song(ndb.Model):
    #title = ndb.StringProperty(required=True)

    @property
    def toJSON(self):
        from songs_routes import bp_songs
        aux={ 'title':str(self.key.id()),      
              'url':url_for('bp_songs.manager_song', urlsafeSong=self.key.urlsafe(), _external=True)}
        return aux
        
    @classmethod
    def getAll(self):
        auxSongsList = []
        for itSongs in Song.query():
            auxSongsList.append(itSongs.to_dict())
        return auxSongsList
    
    @classmethod
    def toJSONlist(self, listSongs):
        listJSON = []
        for itSongs in listSongs:
            listJSON.append(itSongs.toJSON)
        return listJSON


    
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
