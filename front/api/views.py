# import time
# from flask import Flask, jsonify, request, Response, abort

# #  app = Flask(__name__)


# def _time2etag(stamp=None):
#     if stamp is None:
#         stamp = time.time()
#     return str(int(stamp * 1000))


# _USERS = {'1': {'name': 'Tarek', 'modified': _time2etag()}}


# def get_user(user_id):
#     if user_id not in _USERS:
#         return abort(404)
#     user = _USERS[user_id]
#     # Zwrócenie kodu 304 w przypadku zgodności nagłówka If-None-Match.
#     if user['modified'] in request.if_none_match:
#         return Response(status=304)
#     resp = jsonify(user)
#     # Wpisanie wartości do nagłówka ETag.
#     resp.set_etag(user['modified'])
#     return resp

import requests
import couchdb
import os
import flask
import bcrypt


class UserProvider(object):
    def __init__(self):
        pass

    def create_user(self, data):
        return data, 201

    def search_user(self, data):
        return data, 201

    def read_user(self, user_id):
        return {}, 200
