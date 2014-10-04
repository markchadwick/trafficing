from flask import Flask
from flask.ext.script import Manager
from flask_injector import FlaskInjector
from injector import Injector
from injector import Module
from injector import singleton
from os import getenv

from api.v1.module import ApiV1Module
from module import AppModule
from module import DbModule
import config


class ManagerModule(Module):
  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    binder.bind(Manager, to=Manager(self._app), scope=singleton)


def create_injector(*ext_modules):
  config_file = getenv('APP_CONFIG') or config.abs('development.py')
  parent = Injector([AppModule(config_file)])
  app = parent.get(Flask)

  modules = [
    DbModule(app),
    ManagerModule(app),
    ApiV1Module(app),
  ]

  injector = FlaskInjector(app, modules + list(ext_modules), parent)
  injector.get = injector.injector.get
  return injector


def main():
  injector = create_injector()
  injector.get(Manager).run()


if __name__ == '__main__':
  main()
