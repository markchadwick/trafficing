from flask.ext.testing import TestCase as FlaskTest

from api import app_and_injector
from config import abs




class TestCase(FlaskTest):

  def modules(self):
    return []

  def create_app(self):
    config_file   = abs('test.py')
    app, injector = app_and_injector(config_file, *self.modules())

    injector.install_into(self)
    self.injector = injector

    return app


from model_test import ModelTest
