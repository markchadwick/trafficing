from flask.ext.sqlalchemy import SQLAlchemy
from injector import Module
from injector import singleton


class DbModule(Module):

  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    binder.bind(SQLAlchemy, to=SQLAlchemy(self._app), scope=singleton)
