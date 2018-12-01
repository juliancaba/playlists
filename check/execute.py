#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

import requests

PRINTER_ENDPOINT = 'http://localhost:4567/webhook'
BACKEND_CONFIG = 'http://localhost:8080/webhook'
BACKEND_SONG = 'http://localhost:8080/songs'
BACKEND_PLAYLIST = 'http://localhost:8080/playlists'
BACKEND_ALBUM = 'http://localhost:8080/albums'
BACKEND_SEARCH = 'http://localhost:8080/search'
BACKEND_SEARCHGQL = 'http://localhost:8080/searchGQL'


# Es posible separarlo por espacios
requests.post(BACKEND_CONFIG, json={'endpoint':PRINTER_ENDPOINT,'genre':'rock'})


responseAdd0=requests.post(BACKEND_ALBUM, json={'title':'Highway to Hell', 'artist':'ACDC', 'genre':'rock'})
print str(responseAdd0.json()['created'])

responseAdd1=requests.post(BACKEND_ALBUM, json={'title':'1989','artist':'Taylor Swift', 'genre':'pop'})
print responseAdd1.json()['created']

responseAdd2=requests.post(BACKEND_SONG, json={'title':'Highway to Hell','album':'Highway to Hell'})
print str(responseAdd2.json()['created'])
responseAdd3=requests.post(BACKEND_SONG, json={'title':'Shake it off', 'album':'1989'})
print responseAdd3.json()['created']
responseAdd4=requests.post(BACKEND_SONG, json={'title':'Bad blood', 'album':'1989'})
print responseAdd4.json()['created']


responseGet1=requests.get(BACKEND_SONG)
print responseGet1.json()


responseGet1=requests.get(BACKEND_ALBUM+'/'+responseAdd0.json()['created'])
print responseGet1.json()


responseDel1=requests.delete(BACKEND_ALBUM+'/'+responseAdd1.json()['created'])
print responseDel1.json()['deleted']


responseGet2=requests.get(BACKEND_SONG+'?album=Highway%20to%20Hell')
print responseGet2.json()


responseGet3=requests.get(BACKEND_SEARCH+'?artist=ACDC')
print responseGet3.json()


responseGet4=requests.get(BACKEND_SEARCHGQL+'?artist=ACDC')
print responseGet4.json()
