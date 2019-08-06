import time

from flask import request

from .models import User


class UserProvider(object):
    def __init__(self):
        pass

    def create_user(self, data):
        return data, 201

    def search_user(self, data):
        return data, 201

    def read_user(self, user_id):
        return {}, 200


class AuthProvider(object):

    def __init__(self):
        pass

    def register(self, data):
        user = User.query.filter(User.email == data.get('email') or User.username == data.get('username')).first()
        if user:
            return {
                       'status': 'fail',
                       'message': 'User already exists. Please Log in. or remind password by email',
                   }, 401
        else:
            try:
                user = User(**data)
                user.save()
                auth_token = user.encode_auth_token(user.id)

                return {
                           'status': 'success',
                           'message': 'Successfully registered.',
                           'auth_token': auth_token.decode()
                       }, 201
            except Exception:
                return {
                           'status': 'fail',
                           'message': 'Some error occurred. Please try again.'
                       }, 500

    def login(self, data):
        try:
            user = User.query.filter(User.email == data.get('email') or User.username == data.get('username')).first()
            if not user:
                return {
                           'status': 'fail',
                           'message': 'User does not exist.',
                       }, 404

            auth_token = user.encode_auth_token(user.id)
            return {
                       'status': 'success',
                       'message': 'Successfully logged in.',
                       'auth_token': auth_token.decode()
                   }, 200
        except Exception:
            return {
                       'status': 'fail',
                       'message': 'Try again'
                   }, 500

    def verify(self):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                return {
                           'status': 'success',
                           'data': {
                               'id': user.id,
                               'email': user.email,
                               'admin': user.admin,
                               'created': user.created,
                               'username': user.username
                           }
                       }, 200
            return {
                       'status': 'fail',
                       'message': resp
                   }, 401
        else:
            return {
                       'status': 'verify fail',
                       'message': 'Provide a valid auth token.'
                   }, 500

    def logout(self):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                auth_token = user.encode_auth_token(user.id, -10)
                time.sleep(3)
                return {
                           'status': 'success',
                           'message': 'Successfully logged out.',
                           'auth_token': auth_token.decode()
                       }, 200
            return {
                       'status': 'fail',
                       'message': resp
                   }, 401
        else:
            return {
                       'status': 'verify fail',
                       'message': 'Signature expired. Please log in again.'
                   }, 500
