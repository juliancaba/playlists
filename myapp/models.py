#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from flask import url_for
from . import db

songs_tab = db.Table('songs_tab',
    db.Column('song_id', db.String(64), db.ForeignKey('songs.idSong')),
    db.Column('playlist_id', db.String(64), db.ForeignKey('playlists.name'))
)


class Song(db.Model):
    __tablename__ = 'songs'
    idSong = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    artist = db.Column(db.String(40), nullable=False)
    album = db.Column(db.String(40), nullable=False)
    year = db.Column(db.Integer)
    
    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):        
        return dict([ (c, getattr(self, c)) for c in self.columns ])

    
class Playlist(db.Model):
    __tablename__ = 'playlists'
    name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(150))
    songs_lst = db.relationship('Song', secondary=songs_tab)
    
    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]
    @property
    def toJSON(self):
        from songs_routes import bp_song
        aux = dict([ (c, getattr(self, c)) for c in self.columns ])
        aux_lst = []
        for it in self.songs_lst:
            aux_lst.append(url_for('bp_song.manager_song', id_song=it, _external=True))
        aux['songs']=aux_lst
        return aux
