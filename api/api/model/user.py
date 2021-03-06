from flask.ext.sqlalchemy import SQLAlchemy
from hashlib import sha1
from injector import inject
from random import random
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.model import Base
from api.model import Collection
from api.model import WithPublicId


class User(Base, WithPublicId):
  __tablename__ = 'logins'

  account_id = Column(String, ForeignKey('users.id'), nullable=False)
  email      = Column(String(255), nullable=False, unique=True)
  password   = Column(String(255), nullable=False)

  account = relationship('Account',
              backref=backref('users', cascade='all,delete'))

  def set_password(self, password, algo='sha1'):
    """
    Set the encrypted password of this user based on the given clear text
    password.
    """
    algo = 'sha1'
    salt = sha1(str(random())).hexdigest()[:5]
    hsh = sha1(salt+password).hexdigest()
    self.password = '%s$%s$%s' % (algo, salt, hsh)


class Users(Collection):

  @inject(db=SQLAlchemy)
  def __init__(self, db):
    super(Users, self).__init__(User, db)

  def authenticate(self, email, password):
    """
    A rough approximation of Django's built-in authentication mechanism. Queries
    the DB for an account with the given email, and checks to see if the hash of
    the password is equal to the one supplied.
    """
    lc = func.lower
    login = self.query.filter(lc(User.email) == lc(email)).first()
    if not login or not login.password:
      return None

    algo, salt, hsh = login.password.split('$')

    if algo == 'sha1':
      digest = sha1(salt + password).hexdigest()
      if digest == hsh:
        return login
      else:
        return None
    else:
      raise ValueError('Unknown password algo, %s' % algo)
