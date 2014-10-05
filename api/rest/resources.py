from flask import Blueprint

from rest.resource import Resource


class Resources(object):

  def __init__(self, name, resources):
    self._name = name

    self._resources = []
    for root, resourceCls in resources:
      resource = Resource(resourceCls, root)
      self._resources.append(resource)

  def bind(self, app, url_prefix):
    blueprint = Blueprint(self._name, __name__)
    for resource in self._resources:
      resource.bind(blueprint)
    app.register_blueprint(blueprint, url_prefix=url_prefix)

