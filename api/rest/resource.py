from flask_injector import request
from injector import Injector
from injector import Key
from injector import inject


ReadSchema  = Key('resource.schema.read')
Instance    = Key('resource.instance')
MethodName  = Key('resource.methodname')
WriteSchema = Key('resource.schema.write')


class Resource(object):
  handlers = [
    ('',      'get',              ['GET']),
    ('',      'create_singleton', ['POST']),
    ('/',     'list',             ['GET']),
    ('/',     'create',           ['POST']),
    ('/<id>', 'update_by_id',     ['PUT']),
    ('/<id>', 'get_by_id',        ['GET']),
    ('/<id>', 'delte_by_id',      ['DELETE']),
  ]

  def __init__(self, cls, root):
    self.root = root
    self.name = getattr(cls, 'name', cls.__name__)

    self._cls = cls
    self._read_schema  = self._get_schema('consumes')
    self._write_schema = self._get_schema('produces')

  def bind(self, blueprint):
    for path, name, methods in Resource.handlers:
      self._register(path, name, methods, blueprint)

  def _register(self, path, name, methods, blueprint):
    if not hasattr(self._cls, name):
      return

    url      = self.root + path
    endpoint = self.name + '#' + name

    from rest.handler import Handler
    @inject(parent=Injector, resource=self._cls)
    def handle(parent, resource, *args, **kwargs):
      module    = self._request_module(resource, name)
      injector  = Injector(modules=[module], parent=parent)
      handler   = injector.get(Handler)

      return handler(*args, **kwargs)

    blueprint.add_url_rule(url, endpoint, handle, methods=methods)

  def _request_module(self, instance, method_name):
    def configure(binder):
      binder.bind(Instance, to=instance, scope=request)
      binder.bind(MethodName, to=method_name, scope=request)
      binder.bind(ReadSchema, to=self._read_schema)
      binder.bind(WriteSchema, to=self._write_schema)
    return configure

  def _get_schema(self, named):
    return getattr(self._cls, named,
      getattr(self._cls, 'schema',
        object))
