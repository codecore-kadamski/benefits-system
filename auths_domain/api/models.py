import jwt
import datetime
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from config import key
from .mixins import ActiveRecordsMixin, UserMixin


SECRET_KEY = key



def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def apikey_info_func(auth_token, required_scopes=None):
    return {'sub': decode_auth_token(auth_token)} or None


class BaseModel(ActiveRecordsMixin):
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), unique=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(200), unique=False, nullable=False)
    created = Column(DateTime, index=False, unique=False, nullable=False)
    admin = Column(Boolean, index=False, unique=False, nullable=False)

    def __init__(self, email, username, password, admin=False):
        self.admin = admin
        self.created = datetime.datetime.now()
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    def encode_auth_token(self, user_id, seconds=5):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        return decode_auth_token(auth_token)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
