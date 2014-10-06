from injector import inject

from api.model import Account
from api.model import User
from api.model import Users
from test import ModelTest


class TestUser(ModelTest):

  @inject(users=Users)
  def setUp(self, users):
    super(TestUser, self).setUp()

    self.users   = users
    self.account = Account(name='Test Account')

    self.session.add(self.account)

  def test_get_by_id(self):
    user = User(account=self.account, email='foo@bar.com', password='wrong')
    self.session.add(user)
    self.session.commit()

    user1 = self.users.get(user.id)
    self.assertEquals(user.id, user1.id)

  def test_get_by_email(self):
    user = User(account=self.account, email='a@b.com')
    user.set_password('pants')
    self.session.add(user)
    self.session.commit()

    user1 = self.users.filter_by(email='a@b.com').first()
    user2 = self.users.filter_by(email='z@z.com').first()

    self.assertTrue(user1 is not None)
    self.assertTrue(user2 is None)

    self.assertEquals(user.id, user1.id)

  def test_simple_authentication(self):
    user = User(account=self.account, email='one@two.com')
    user.set_password('test123')

    self.session.add(user)
    self.session.commit()

    authed = self.users.authenticate('one@two.com', 'test123')
    unauthed = self.users.authenticate('one@two.com', 'TEST123')

    self.assertTrue(authed is not None)
    self.assertTrue(unauthed is None)

    self.assertEquals(user.id, authed.id)

  def test_email_case_insensative(self):
    user = User(account=self.account, email='test@example.com')
    user.set_password('test123')
    self.session.add(user)
    self.session.commit()

    authed = self.users.authenticate('TEST@example.com', 'test123')
    self.assertTrue(authed is not None)

    self.assertEquals(user.id, authed.id)
