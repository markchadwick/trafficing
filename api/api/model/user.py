from sqlalchemy.sql import func
from hashlib import sha1

from api.model import WithPublicId
from api.model import db


class Account(db.Model, WithPublicId):
  __tablename__ = 'logins'

  account_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
  email      = db.Column(db.String(255), nullable=False, unique=True)
  password   = db.Column(db.String(255), nullable=False)

  account = db.relationship('User',
              backref=db.backref('users', cascase='all,delete'))

  @classmethod
  def authenticate(cls, email, password):
    """
    A rough approximation of Django's built-in authentication mechanism. Queries
    the DB for an account with the given email, and checks to see if the hash of
    the password is equal to the one supplied.
    """
    lc = func.lower
    login = cls.query.filter(lc(cls.email) == lc(email)).first()
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
