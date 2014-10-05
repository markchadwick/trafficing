from flask import Session
from injector import inject
from schema import And
from schema import Use

from api.model import User
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

  @inject(user=User, session=Session)
  def __init__(self, user, session):
    self.user = user
    self.session = session

  def get(self):
    if self.user is None:
      raise exc.Forbidden()

    return {
      'email': self.user.email,
    }

  def create(self, schema):
    pass
