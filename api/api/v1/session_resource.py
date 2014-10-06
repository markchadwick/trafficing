from flask import Session
from injector import inject
from schema import And
from schema import Use

from api.model import User
from api.model import Users
from rest import exc


class SessionResource(object):
  name = 'session'

  consumes = {
    'email':    And(str, len),
    'password': And(str, len),
  }

  produces = {
    'email':    Use(str)
  }

  @inject(user=User, users=Users, session=Session)
  def __init__(self, user, users, session):
    self.user    = user
    self.users   = users
    self.session = session

  def get(self):
    if self.user is None:
      raise exc.Forbidden()

    return {
      'email': self.user.email,
    }

  def create(self, user):
    user = self.users.authenticate(user['email'], user['password'])
    if user is None:
      raise exc.Forbidden()

    pass
