from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector

from api.module import ApiV1Module
from api.module import AppModule
from api.module import DbModule


def app_and_injector(config_file, *ext_mods):
  parent  = Injector([AppModule(config_file)])
  app     = parent.get(Flask)
  modules = [
    DbModule(app),
    ApiV1Module(app),
  ]

  i = FlaskInjector(app, modules + list(ext_mods), parent)
  return i.app, i.injector
