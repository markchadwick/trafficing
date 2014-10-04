from injector import Module
from injector import singleton

from api.v1 import AccountResource
from rest import Resources


class ApiV1Module(Module):

  resources = [
    ('/account', AccountResource)
  ]

  def __init__(self, app):
    self._app = app

  def configure(self, binder):
    resources = Resources('apiv1', ApiV1Module.resources)

    binder.bind(Resources, to=resources, scope=singleton)

    resources.bind(self._app, '/api/v1')
