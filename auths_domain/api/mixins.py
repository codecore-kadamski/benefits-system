#  from sqlalchemy.orm import Session, scoped_session, Query
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import RelationshipProperty
from flask_login import UserMixin


Base = declarative_base()


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class ModelNotFoundError(ValueError):
    pass


class NoSessionError(RuntimeError):
    pass


class InspectionMixin(Base):
    __abstract__ = True

    @classproperty
    def columns(cls):
        return inspect(cls).columns.keys()

    @classproperty
    def primary_keys_full(cls):
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = cls.__mapper__
        return [
            mapper.get_property_by_column(column)
            for column in mapper.primary_key
        ]

    @classproperty
    def primary_keys(cls):
        return [pk.key for pk in cls.primary_keys_full]

    @classproperty
    def relations(cls):
        """Return a `list` of relationship names or the given model
        """
        return [c.key for c in cls.__mapper__.iterate_properties
                if isinstance(c, RelationshipProperty)]

    @classproperty
    def settable_relations(cls):
        """Return a `list` of relationship names or the given model
        """
        return [r for r in cls.relations
                if getattr(cls, r).property.viewonly is False]

    @classproperty
    def hybrid_properties(cls):
        items = inspect(cls).all_orm_descriptors
        return [item.__name__ for item in items
                if type(item) == hybrid_property]

    @classproperty
    def hybrid_methods_full(cls):
        items = inspect(cls).all_orm_descriptors
        return {item.func.__name__: item
                for item in items if type(item) == hybrid_method}

    @classproperty
    def hybrid_methods(cls):
        return list(cls.hybrid_methods_full.keys())


class SessionMixin:
    _session = None

    @classmethod
    def set_session(cls, session):
        """
        :type session: scoped_session | Session
        """
        cls._session = session

    @classproperty
    def session(cls):
        """
        :rtype: scoped_session | Session
        """
        if cls._session is not None:
            return cls._session
        else:
            raise NoSessionError('Cant get session.'
                                 'Please, call SaActiveRecord.set_session()')

    @classproperty
    def query(cls):
        """
        :rtype: Query
        """
        return cls.session.query(cls)


class ActiveRecordsMixin(InspectionMixin, SessionMixin):
    __abstract__ = True

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    def save(self):
        """Saves the updated model to the current entity db.
        """
        self.session.add(self)
        self.session.commit()
        self.session.flush()
        return self

    @classmethod
    def create(cls, **kwargs):
        """Create and persist a new record for the model
        :param kwargs: attributes for the record

        :return: the new model instance
        """
        return cls().fill(**kwargs).save()

    def update(self, **kwargs):
        """Same as :meth:`fill` method but persists changes to database.
        """
        return self.fill(**kwargs).save()

    def delete(self):
        """Removes the model from the current entity session and mark for deletion.
        """
        self.session.delete(self)
        self.session.commit()
        self.session.flush()

    @classmethod
    def destroy(cls, *ids):
        """Delete the records with the given ids
        :type ids: list
        :param ids: primary key ids of records
        """
        for pk in ids:
            cls.find(pk).delete()
        cls.session.flush()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def first(cls):
        return cls.query.first()

    @classmethod
    def find(cls, id_):
        """Find record by the id
        :param id_: the primary key
        """
        return cls.query.get(id_)

    @classmethod
    def find_or_fail(cls, id_):
        # assume that query has custom get_or_fail method
        result = cls.find(id_)
        if result:
            return result
        else:
            raise ModelNotFoundError("{} with id '{}' was not found"
                                     .format(cls.__name__, id_))
