#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-


import json
from flask import Blueprint, jsonify, abort, make_response, request, url_for
from myapp.models import Webhook, db

bp_webhook=Blueprint("bp_webhook", __name__)


@bp_webhook.route('/webhook', methods = ['POST'])
def addWebhook():
    attr = ['endpoint', 'genre']
    if not request.json or [it for it in attr if not it in request.json]:
        abort(400)
    endpoint = request.json['endpoint']
    genre = request.json['genre']

    try:
        auxWH = (Webhook.query.filter_by(idEndpoint=endpoint)).first()
        if not (genre in auxWH.genres):
            auxWH.genres = auxWH.genres+' '+genre
        db.session.commit()
        response=make_response(jsonify({"updated":endpoint}), 200)
    except:
        new_wh = Webhook(
            idEndpoint = endpoint,
            genres=genre)
        try:
            db.session.add(new_wh)
            db.session.commit()
            response= make_response(jsonify({"created":endpoint}), 201)
        except:
            abort(409)
    return response


