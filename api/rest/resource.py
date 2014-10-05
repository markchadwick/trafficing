import json

from flask import Request
from flask import Response
from functools import wraps
from injector import inject
from schema import Schema

from rest import Codec
from rest import exc


class Resource(object):
  handlers = [
    ('',      'get',          ['GET']),
    ('/',     'list',         ['GET']),
    ('/',     'create',       ['POST']),
    ('/<id>', 'update_by_id', ['PUT']),
    ('/<id>', 'get_by_id',    ['GET']),
    ('/<id>', 'delte_by_id',  ['DELETE']),
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

    @self._parse_request
    @inject(resource=self._cls)
    def handle(resource, *args, **kwargs):
      return self._handle(getattr(resource, name), args, kwargs)

    url = self._url(path)
    endpoint = self._endpoint(name)
    blueprint.add_url_rule(url, endpoint, handle)

  def _url(self, relative):
    return self.root + relative

  def _endpoint(self, name):
    return self.name + '#' + name

  def _get_schema(self, named):
    return getattr(self._cls, named, getattr(self._cls, 'schema', {}))

  def _handle(self, func, args, kwargs):
    try:
      result = func(*args, **kwargs)
      Schema(self._write_schema).validate(result)
      return json.dumps(result)
    except exc.RestException, e:
      html = '<h1>%s</h1>' % e.message
      return Response(status=e.status, response=html)

  def _parse_request(self, func):
    """
    In the case of a PUT or POST request, parse the body, and deserialize it
    using the current codec. The deserialized object will be validated and
    passed the the wrapped function.
    """
    @wraps(func)
    @inject(request=Request, codec=Codec)
    def parse(request, codec, *args, **kwargs):
      method = request.method
      if method == 'PUT' or method == 'POST':
        try:
          data = codec.decode(request.data)
        except Exception, e:
          raise exc.BadRequest({'error': e.message})
        return func(data, *args, **kwargs)
      else:
        return func(*args, **kwargs)

    return parse

  def _flask_response(self, func):
    """
    Decorator that wraps a function call to return a Flask response. It's
    assumed that the function will either return a simple object, or raise an
    exception. If a `RestException` is thrown, it will use its status code and
    any `toObject` message semantics, otherwise, a simple 500 message will be
    returned.
    """
    @wraps(func)
    @inject(codec=Codec)
    def resp(codec, *args, **kwargs):
      try:
        response = func(*args, **kwargs)
        return codec.response(200, response)
      except exc.RestException, e:
        return Response(e.status, e.toObject())
      except Exception, e:
        return Response(500, {'error', e.message})
    return resp

