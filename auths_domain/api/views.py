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
            }, 202
        else:
            try:
                user = User(**data)
                user.save()
                auth_token = user.encode_auth_token(user.id)
                return {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
            except Exception:
                return {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
