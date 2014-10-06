from flask import Flask
from flask import Request
from flask import Session
from flask import globals
from flask_cors import CORS
from flask_injector import request
from injector import Module
from injector import inject
from injector import provides
from injector import singleton

from api.model import User
from api.v1 import SessionResource
from rest import Codec
from rest import JsonCodec


class AppModule(Module):

  def __init__(self, config_file):
    self._config_file = config_file

  @singleton
  @provides(Flask)
  def provide_app(self):
    app = Flask(__name__)
    app.config.from_pyfile(self._config_file)

    CORS(app, resources={r'/api/*': {'origins': '*'}})
    return app

  @provides(Session)
  @request
  def provide_session(self):
    top = globals._request_ctx_stack.top
    return top.session

  @provides(User)
  @request
  @inject(sessions=SessionResource)
  def provide_current_user(self, sessions):
    return sessions.user

  @provides(Codec)
  @request
  @inject(request=Request)
  def provide_codec(self, request):
    return JsonCodec()
