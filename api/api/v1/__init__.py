from flask import Blueprint
from injector import inject
from flask.ext.sqlalchemy import SQLAlchemy

from api.model import Account

v1 = Blueprint('v1', __name__)


@v1.route('/hi')
@inject(db=SQLAlchemy)
def say_hi(db):
  for account in db.session.query(Account).all():
    print account.id
  return 'there'


def init(app):
  app.register_blueprint(v1, url_prefix='/api/v1')
