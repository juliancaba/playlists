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
def delSong(id_song):
    aux = list(filter(lambda t:t['id'] == id_song, songs))
    if len(aux) == 0:
        abort(404)
    songs.remove(aux[0])
    return make_response(jsonify({"deleted":id_song}), 200)


def getSong(id_song):
    aux = list(filter(lambda t:t['id'] == id_song, songs))
    if len(aux) == 0:
        abort(404)
    return make_response(jsonify({"song":aux[0]}), 200)


@app.route('/songs/<path:id_song>', methods = ['DELETE','GET'])
def manager_song(id_song):
    if request.method == 'DELETE':
        return delSong(id_song)
    elif request.method == 'GET':
        return getSong(id_song)



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


@app.route('/playlists/<path:id_ps>', methods = ['DELETE', 'PUT', 'GET'])
def manager_playlist(id_ps):
    if request.method == 'GET':
        return getPlaylist(id_ps)
    elif request.method == 'PUT':
        return addPlaylist(id_ps)
    elif request.method == 'DELETE':
        return delPlaylist(id_ps)


@app.route('/playlists/<id_ps>/songs', methods = ['POST'])
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
    hateoasSong = url_for('manager_song', id_song=reqSong, _external=True)
    if hateoasSong in lstPS[0]['songs']:
        abort(409)
        
    lstPS[0]['songs'].append(hateoasSong)
        
    return jsonify({"info":"Added "+ reqSong + " in " + id_ps + " playlist"})


@app.route('/playlists/<id_ps>/songs/<id_song>', methods = ['DELETE'])
def delSongOfAPlaylist(id_ps, id_song):
    auxPS = list(filter(lambda t:t['name'] == id_ps, playlists))
    if len(auxPS) == 0:
        abort(404)

    psSongs = auxPS[0]['songs']
    hateoasSong = url_for('manager_song', id_song=id_song, _external=True)
    
    auxS = list(filter(lambda t:t == hateoasSong, psSongs))
    if len(auxS) == 0:
        abort(404)
        
    auxPS[0]['songs'].remove(auxS[0])
        
    return jsonify({"info":"Deleted "+ id_song + " from " + id_ps + " playlist"})
    


if __name__ == '__main__':
    app.run(debug=True)


