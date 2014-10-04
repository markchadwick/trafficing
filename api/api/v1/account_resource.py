from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject
from json import dumps

from api.model import Account


class AccountResource(object):
  name = 'account'

  @inject(db=SQLAlchemy)
  def __init__(self, db):
    self.accounts = db.session.query(Account)

  def list(self):
    res = []
    for account in self.accounts:
      res.append(self._to_simple(account))
    return dumps(res)

  def get(self, id):
    account = self.accounts.get(id)
    return dumps(self._to_simple(account))

  def _to_simple(self, account):
    return {
      'id':     account.id,
      'url':    url_for('apiv1.account_get', id=account.id),
      'email':  account.email,
      'name':   account.name
    }
