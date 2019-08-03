from .models import UserModel


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

    def __call__(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        pass

    def register(self, data):
        return {'register': True}, 201
