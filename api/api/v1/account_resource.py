from flask import url_for
from injector import inject

from api.model import Accounts


class AccountResource(object):
  name = 'account'

  @inject(accounts=Accounts)
  def __init__(self, accounts):
    self.accounts = accounts

  def list(self):
    res = []
    for account in self.accounts.query:
      res.append(self._to_simple(account))
    return res

  def get_by_id(self, id):
    account = self.accounts.query.get(id)
    return self._to_simple(account)

  def _to_simple(self, account):
    return {
      'id':     account.id,
      'url':    url_for('apiv1.account#get_by_id', id=account.id),
      'email':  account.email,
      'name':   account.name
    }
