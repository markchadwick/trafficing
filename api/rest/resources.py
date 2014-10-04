from flask import Blueprint
from injector import inject


class Resources(object):

  def __init__(self, name, resources):
    self._blueprint = Blueprint(name, __name__)

    for root, resourceCls in resources:
      self._register_list(root, resourceCls)
      self._register_get(root, resourceCls)

  def bind(self, app, url_prefix):
    app.register_blueprint(self._blueprint, url_prefix=url_prefix)

  def _register_list(self, root, resourceCls):
    if not getattr(resourceCls, 'list'):
      return

    url  = '%s/' % (root)
    name = '%s_list' % resourceCls.name

    @inject(resource=resourceCls)
    def list(resource):
      return resource.list()

    self._blueprint.add_url_rule(url, name, list)

  def _register_get(self, root, resourceCls):
    if not getattr(resourceCls, 'get'):
      return

    url  = '%s/<id>' % (root)
    name = '%s_get' % resourceCls.name

    @inject(resource=resourceCls)
    def get(id, resource):
      return resource.get(id)

    self._blueprint.add_url_rule(url, name, list)
