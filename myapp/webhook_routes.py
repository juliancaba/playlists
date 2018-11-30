#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from google.appengine.ext import ndb
from myapp.models import Webhook

bp_webhook=Blueprint("bp_webhook", __name__)


@bp_webhook.route('/webhook', methods = ['POST'])
def addWebhook():
    attr = ['endpoint', 'genre']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    endpoint = request.json['endpoint']
    genre = request.json['genre']
    
    try:
        keyWH = ndb.Key('Webhook', endpoint)
        auxWH = keyWH.get()
        if not (genre in auxWH.genres):
            auxWH.genres.append(genre)
        auxWH.put()
        response=make_response(jsonify({"updated":endpoint}), 200)
    except:
        newWebhook = Webhook(
            id = endpoint,
            genres=[genre])
        try:
            newWebhook.put()
            response= make_response(jsonify({"created":endpoint}), 201)
        except:
            abort(409)
    return response


