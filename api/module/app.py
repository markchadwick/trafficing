from flask import Flask
from injector import Module
from injector import provides
from injector import singleton


class AppModule(Module):

  def __init__(self, config_file):
    self._config_file = config_file

  @singleton
  @provides(Flask)
  def provide_app(self):
    app = Flask(__name__)
    app.config.from_pyfile(self._config_file)

    return app
