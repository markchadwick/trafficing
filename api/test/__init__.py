from flask.ext.testing import TestCase as FlaskTest
from injector import Module

from api import app_and_injector
from config import abs
from rest import Codec
from rest import JsonCodec


class TestModule(Module):
  def configure(self, binder):
    binder.bind(Codec, to=JsonCodec)

class TestCase(FlaskTest):

  def modules(self):
    return []

  def app_modules(self, app):
    return []

  def create_app(self):
    config_file   = abs('test.py')
    app, injector = app_and_injector(config_file, *self.modules())

    for module in self.app_modules(app):
      injector.binder.install(module)
    injector.install_into(self)
    self.injector = injector

    return app


from model_test import ModelTest
