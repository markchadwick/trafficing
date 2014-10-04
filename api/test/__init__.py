from flask import Flask
from flask.ext.testing import TestCase as FlaskTest
from injector import Injector

from module import AppModule
from module import DbModule
import config


class TestCase(FlaskTest):

  def __init__(self, *args, **kwargs):
    super(TestCase, self).__init__(*args, **kwargs)

    self._injector = Injector([
      AppModule(config.abs('test.py')),
      DbModule()
    ])

  def create_app(self):
    return self._injector.get(Flask)


from model_test import ModelTest
