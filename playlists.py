#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import base64
import json
from flask import Flask, jsonify, abort, make_response, request, url_for
app = Flask(__name__)
app.config['DEBUG'] = True

'''
songs = [{"id":md5, base64 --> title and album,
          "title":"",
          "artist":"",
          "album": "",
          "year":""}]

playlist = [{"name":"",
             "description":"",
             "songs":[]}]
'''

songs = []
playlists = []



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


# OPERACIONES sobre songs
def delSong(idSong):
    auxSong = list(filter(lambda t:t['id'] == idSong, songs))
    if len(auxSong) == 0:
        abort(404)
    songs.remove(auxSong[0])
    return make_response(jsonify({"deleted":idSong}), 200)


def getSong(idSong):
    listSong = list(filter(lambda t:t['id'] == idSong, songs))
    if len(listSong) == 0:
        abort(404)
    return make_response(jsonify(listSong[0]), 200)


@app.route('/songs/<path:idSong>', methods = ['DELETE','GET'])
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


@app.route('/songs', methods = ['GET', 'POST'])
def manager_songs():
    if request.method == 'POST':
        return addSong()
    elif request.method == 'GET':
        return getSongs()



# OPERACIONES sobre playlists

@app.route('/playlists', methods = ['GET'])
def getPlaylists():
    return make_response(jsonify({"playlists":playlists}), 200)


def delPlaylist(idPlaylist):    
    listPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))
    if len(listPlaylist) == 0:
        abort(404)
    playlists.remove(listPlaylist[0])
    return make_response(jsonify({'deleted':listPlaylist[0]['name']}), 200)


def getPlaylist(idPlaylist):    
    listPlaylist = list(filter(lambda t:t['name'] == str(idPlaylist), playlists))
    if len(listPlaylist) == 0:
        abort(404)
    return make_response(jsonify(listPlaylist[0]), 200)


def addPlaylist(idPlaylist):
    listPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))

    description = ""
    if request.json and 'description' in request.json:
        description = request.json['description']

    if len(listPlaylist) != 0:
        listPlaylist[0]['description'] = description
        listPlaylist[0]['songs'] = []
        return make_response(jsonify({"updated":str(idPlaylist)}), 200)
        
    newPlaylist = {
        'name' : idPlaylist,
        'description':description,
        'songs':[]}
    playlists.append(newPlaylist)
    return make_response(jsonify({"created":str(idPlaylist)}), 201)


@app.route('/playlists/<path:idPlaylist>', methods = ['DELETE', 'PUT', 'GET'])
def manager_playlist(idPlaylist):
    if request.method == 'GET':
        return getPlaylist(idPlaylist)
    elif request.method == 'PUT':
        return addPlaylist(idPlaylist)
    elif request.method == 'DELETE':
        return delPlaylist(idPlaylist)


@app.route('/playlists/<idPlaylist>', methods = ['POST'])
@app.route('/playlists/<idPlaylist>/songs', methods = ['POST'])
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
    hateoasSong = url_for('manager_song', idSong=idSong, _external=True)
    if hateoasSong in listPlaylist[0]['songs']:
        abort(409)
        
    listPlaylist[0]['songs'].append(hateoasSong)
        
    return make_response(("Added "+ idSong + " in " + idPlaylist + " playlist"), 200)


@app.route('/playlists/<idPlaylist>/<idSong>', methods = ['DELETE'])
@app.route('/playlists/<idPlaylist>/songs/<idSong>', methods = ['DELETE'])
def delSongOfAPlaylist(idPlaylist, idSong):
    listPlaylist = list(filter(lambda t:t['name'] == idPlaylist, playlists))
    if len(listPlaylist) == 0:
        abort(404)

    listSongsPlaylist = listPlaylist[0]['songs']
    hateoasSong = url_for('manager_song', idSong=idSong, _external=True)
    
    auxListSongs = list(filter(lambda t:t == hateoasSong, listSongsPlaylist))
    if len(auxListSongs) == 0:
        abort(404)
        
    listPlaylist[0]['songs'].remove(auxListSongs[0])
        
    return make_response(("Deleted "+ idSong + " from " + idPlaylist + " playlist"), 200)
    


if __name__ == '__main__':
    app.run(debug=True)


