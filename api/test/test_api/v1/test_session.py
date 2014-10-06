from flask import Session
from injector import inject
from nose.tools import raises

from api.model import Account
from api.model import User
from api.model import Users
from api.v1 import SessionResource
from rest import exc
from test import ModelTest


class TestSessionResource(ModelTest):

  @inject(users=Users, res=SessionResource)
  def setUp(self, users, res):
    super(TestSessionResource, self).setUp()

    self.users = users
    self.res   = res

    account = Account(name='Default')
    user = User(account=account, email='scott@oracle.com')
    user.set_password('tiger')

    self.session.add(user)
    self.session.commit()
    self.user = user

  @raises(exc.Forbidden)
  def test_get(self):
    self.res.get()

  @raises(exc.Forbidden)
  def test_bad_login(self):
    self.res.create({
      'email':    'scott@oracle.com',
      'password': 'not-tiger',
    })

  def test_create(self):
    session = self.res.create({
      'email':    'scott@oracle.com',
      'password': 'tiger',
    })
    self.assertEquals({'email': 'scott@oracle.com'}, session)

  @inject(session=Session)
  def test_session_gets_user_id(self, session):
    self.assertEquals({}, session)
    self.res.create({
      'email':    'scott@oracle.com',
      'password': 'tiger',
    })

    self.assertEquals({'user_id': self.user.id}, session)

  @inject(session=Session)
  def test_delete(self, session):
    self.assertFalse('user_id' in session)

    self.res.user = self.user
    self.assertTrue('user_id' in session)

    self.res.delete()
    self.assertFalse('user_id' in session)
