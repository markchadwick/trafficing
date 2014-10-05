import json

from abc import ABCMeta
from abc import abstractmethod
from flask import Response
from functools import wraps
from werkzeug.datastructures import Headers


class Codec(object):
  __metaclass__ = ABCMeta

  content_type = 'text/plain'

  @abstractmethod
  def encode(self, payload): pass

  @abstractmethod
  def decode(self, payload): pass

  def __call__(self, func):
    """
    Wraps as method so that its aruments are appended with the decdoded results
    of its call, and its results are encoded with the same codec
    """
    @wraps(func)
    def wrapped(payload, *args, **kwargs):
      req = self.decode(payload)
      res = func(req, *args, **kwargs)
      return self.encode(res)

    return wrapped

  def response(self, status, obj, headers=None):
    if headers is None:
      headers = Headers()

    content_type = self.__class__.content_type
    headers.add('Content-Type', content_type)

    response = self.encode(obj)
    return Response(status=status, headers=headers, response=response)


class JsonCodec(Codec):
  content_type = 'text/plain'

  def encode(self, payload):
    return json.dumps(payload)

  def decode(self, payload):
    return json.loads(payload)
