from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject
from json import dumps

from api.model import Account


class AccountResource(object):
  name = 'account'

  @inject(db=SQLAlchemy)
  def __init__(self, db):
    self._db = db

  def list(self):
    res = []
    for account in self._db.session.query(Account):
      res.append(self._to_simple(account))
    return dumps(res)

  def get(self, id):
    account = self._db.session.query(Account).get(id)
    return self._to_simple(account)

  def _to_simple(self, account):
    return {
      'id':     account.id,
      'url':    url_for('apiv1.account_get', id=account.id),
      'email':  account.email,
      'name':   account.name
    }
