import datetime
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class BaseModel(Base):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class UserModel(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(200), unique=False, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    age = Column(Integer, unique=False, nullable=True)
    created = Column(DateTime, index=False, unique=False, nullable=False)
    admin = Column(Boolean, index=False, unique=False, nullable=False)

    def __init__(self, *args, **kw):
        super(UserModel, self).__init__(*args, **kw)
        self._authenticated = False

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
