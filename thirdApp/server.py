#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

from flask import Flask, request, make_response
import requests

app = Flask(__name__)


    
@app.route('/webhook', methods=['POST'])
def webhook():
    print request.data
    return make_response("",200)



if __name__ == '__main__':
    app.run(debug=True, port=4567)
