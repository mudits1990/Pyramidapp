from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    String,
    UnicodeText,
    VARCHAR,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
import transaction
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class _BaseMixin(object):
    """
    A helper mixin class to set properties on object creation.

    Also provides a convenient default __repr__() function, but be aware that
    also relationships are printed, which might result in loading the relation
    objects from the database

    Also contains the get_by_id method
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        try:
            val = "<%s(%s)>" % (self.__class__.__name__,
                                ', '.join('%s=%r' % (k, str(self.__dict__[k])[0:25])
                                          for k in sorted(self.__dict__)
                                          if '_' != k[0]
                                    #if '_sa_' != k[:4] and '_backref_' != k[:9]
                                )
            )
        except UnicodeEncodeError:
            return self.__class__.__name__
        return val

    @classmethod
    def get_by_id(cls, obj_id):
        return DBSession.query(cls).filter(cls.id == obj_id).first()

    def save_obj(self, commit=False):
        DBSession.add(self)
        transaction.commit()
        return self

    def delete_obj(self, commit=False):
        DBSession.delete(self)
        transaction.commit()
        return self


class MyModel(Base, _BaseMixin):
    __tablename__ = 'userAuth'
    id = Column(String(100), primary_key=True)
    access_token = Column(UnicodeText)
    refresh_token = Column(UnicodeText)
    instance_url = Column(UnicodeText)

Index('my_index', MyModel.access_token, unique=True, mysql_length=255)
