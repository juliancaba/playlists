#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

import json
import requests

PRINTER_ENDPOINT = 'http://localhost:4567/webhook'
BACKEND_CONFIG = 'http://localhost:5000/webhook'
BACKEND_SONG = 'http://localhost:5000/songs'


# Es posible separarlo por espacios
requests.post(BACKEND_CONFIG, json={'endpoint':PRINTER_ENDPOINT,'genre':'rock'})
requests.post(BACKEND_CONFIG, json={'endpoint':PRINTER_ENDPOINT,'genre':'pop'})


response1=requests.post(BACKEND_SONG, json={'title':'Highway to Hell','artist':'ACDC', 'album':'Highway to Hell', 'genre':'rock'})
print(str(response1.json()['created']))
response2=requests.post(BACKEND_SONG, json={'title':'Shake it off','artist':'Taylor Swift', 'album':'Shake it off', 'genre':'pop'})
print(response2.json()['created'])
response3=requests.post(BACKEND_SONG, json={'title':'Little Big Town','artist':'Better Man', 'album':'The Breaker', 'genre':'country'})
print(response3.json()['created'])
response4=requests.post(BACKEND_SONG, json={'title':'Blending Love','artist':'Leona Lewis', 'album':'Spirit'})
print(response4.json()['created'])


    
