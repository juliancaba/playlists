#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

import requests

PRINTER_ENDPOINT = 'http://localhost:4567/webhook'
BACKEND_CONFIG = 'http://localhost:8080/webhook'
BACKEND_SONG = 'http://localhost:8080/songs'
BACKEND_PLAYLIST = 'http://localhost:8080/playlists'


# Es posible separarlo por espacios
requests.post(BACKEND_CONFIG, json={'endpoint':PRINTER_ENDPOINT,'genre':'rock'})
requests.post(BACKEND_CONFIG, json={'endpoint':PRINTER_ENDPOINT,'genre':'pop'})

print("Adding songs")
responseAdd1=requests.post(BACKEND_SONG, json={'title':'Highway to Hell','artist':'ACDC', 'album':'Highway to Hell', 'genre':'rock'})
print(str(responseAdd1.json()['created']))
responseAdd2=requests.post(BACKEND_SONG, json={'title':'Shake it off','artist':'Taylor Swift', 'album':'Shake it off', 'genre':'pop'})
print(responseAdd2.json()['created'])
responseAdd3=requests.post(BACKEND_SONG, json={'title':'Little Big Town','artist':'Better Man', 'album':'The Breaker', 'genre':'country'})
print(responseAdd3.json()['created'])
responseAdd4=requests.post(BACKEND_SONG, json={'title':'Blending Love','artist':'Leona Lewis', 'album':'Spirit'})
print(responseAdd4.json()['created'])


print("Get song")
responseGet1=requests.get(BACKEND_SONG+'/'+responseAdd4.json()['created'])
print(responseGet1.json())
    

print("Delete song")
responseDel1=requests.delete(BACKEND_SONG+'/'+responseAdd4.json()['created'])
print(responseDel1.json()['deleted'])
    


print("Add/update playlist")
responseAdd5=requests.put(BACKEND_PLAYLIST+'/ps')
print(str(responseAdd5.json()))
responseUpd1=requests.put(BACKEND_PLAYLIST+'/ps', json={'description':'mi lista'})
print(str(responseUpd1.json()['updated']))

print("Get playlist")
responseGet2=requests.get(BACKEND_PLAYLIST+'/ps')
print(responseGet2.json())


print("Get playlists")
responseGet3=requests.get(BACKEND_PLAYLIST)
print(responseGet3.json())


print("Add song to playlist")
responseUpd2=requests.post(BACKEND_PLAYLIST+'/ps/songs', json={'song':str(responseAdd3.json()['created'])})
print(str(responseUpd2.text))

responseUpd3=requests.post(BACKEND_PLAYLIST+'/ps/songs', json={'song':str(responseAdd2.json()['created'])})
print(str(responseUpd3.text))

responseUpd3=requests.delete(BACKEND_PLAYLIST+'/ps/songs/'+str(responseAdd3.json()['created']))
print(str(responseUpd3.text))

print("Get playlist")
responseGet2=requests.get(BACKEND_PLAYLIST+'/ps')
print(responseGet2.json())

