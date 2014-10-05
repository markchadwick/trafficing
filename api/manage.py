from flask.ext.script import Manager
from injector import Module
from injector import singleton
from os import getenv

import config
from api import app_and_injector


class ManagerModule(Module):
  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    binder.bind(Manager, to=Manager(self._app), scope=singleton)


def create_injector(*ext_modules):
  config_file = getenv('APP_CONFIG') or config.abs('development.py')
  app, injector = app_and_injector(config_file, *ext_modules)
  injector.binder.install(ManagerModule(app))
  return injector


def main():
  injector = create_injector()
  injector.get(Manager).run()


if __name__ == '__main__':
  main()
