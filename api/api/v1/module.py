from injector import Module

from api.v1 import v1


class ApiV1Module(Module):

  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    self._app.register_blueprint(v1, url_prefix='/api/v1')
