from flask.ext.sqlalchemy import SQLAlchemy
from injector import Module
from injector import singleton

from api.model import Base

class DbModule(Module):

  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    db = SQLAlchemy(self._app)
    db.Model = Base
    binder.bind(SQLAlchemy, to=db, scope=singleton)
