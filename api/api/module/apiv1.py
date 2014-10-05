from injector import Module
from injector import singleton

from api.v1 import AccountResource
from api.v1 import SessionResource
from rest import Resources


class ApiV1Module(Module):
  root = '/api/v1'

  resources = [
    ('/account', AccountResource),
    ('/session', SessionResource),
  ]

  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    resources = Resources('apiv1', ApiV1Module.resources)
    binder.bind(Resources, to=resources, scope=singleton)
    resources.bind(self._app, ApiV1Module.root)

