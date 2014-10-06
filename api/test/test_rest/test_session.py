from nose.tools import raises
from test import ModelTest

from api.v1 import SessionResource
from rest import exc


class TestLoggedOut(ModelTest):

  def setUp(self):
    self.res = self.injector.get(SessionResource)

  @raises(exc.Forbidden)
  def test_get(self):
    self.res.get()

  @raises(exc.Forbidden)
  def test_bad_login(self):
    self.res.create({
      'email':    'foo@bar.com',
      'password': 'tiger',
    })

  def test_create(self):
    pass


# class TestLoggedIn(ModelTest):
#   def setUp(self):
#     self.user = User(email='foo@bar.com')
#     self.res = SessionResource(self.user, None)
# 
#   def test_get(self):
#     session = self.res.get()
#     self.assertEquals({'email': 'foo@bar.com'}, session)
