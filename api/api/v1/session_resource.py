from flask import Session
from flask_injector import request
from injector import inject
from schema import And
from schema import Use

from api.model import Users
from rest import exc


@request
class SessionResource(object):
  name = 'session'

  consumes = {
    'email':    And(str, len),
    'password': And(str, len),
  }

  produces = {
    'email':    Use(str)
  }

  @inject(users=Users, session=Session)
  def __init__(self, users, session):
    self.users   = users
    self.session = session
    self._user   = None

  def get(self):
    if self.user is None:
      raise exc.Forbidden()
    return self._to_simple()

  def create_singleton(self, user):
    return self.create(user)

  def create(self, user):
    user = self.users.authenticate(user['email'], user['password'])
    if user is None:
      raise exc.Forbidden()

    self.user = user
    return self._to_simple()

  def delete(self):
    self.user = None

  @property
  def user(self):
    if self._user is not None:
      return self._user

    if 'user_id' in self.session:
      self._user = self.users.get(self.session['user_id'])
      return self._user

  @user.setter
  def user(self, user):
    if user is None:
      self._user = None
      del self.session['user_id']

    else:
      self._user = user
      self.session['user_id'] = user.id

  def _to_simple(self):
    return {
      'email': self.user.email
    }
