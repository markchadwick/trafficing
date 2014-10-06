from flask import Request
from flask_injector import request
from injector import Injector
from injector import inject
from schema import Schema

from rest import Codec
from rest import exc
from rest.resource import Instance
from rest.resource import MethodName
from rest.resource import ReadSchema


@request
class Handler(object):

  @inject(injector=Injector)
  def __init__(self, injector):
    self._injector = injector

  @inject(codec=Codec)
  def __call__(self, codec, *args, **kwargs):
    try:
      request  = self.request()
      response = self.invoke(request=request, args=args, kwargs=kwargs)
      return codec.response(200, response)

    except exc.RestException, e:
      return codec.response(e.status, e.toObject())

    # except Exception, e:
    #   return Response(500, {'error', e.message})

  @inject(request=Request, codec=Codec, schema=ReadSchema)
  def request(self, request, codec, schema):
    """
    In the case of a PUT or POST request, parse the body, and deserialize it
    using the current codec. The deserialized object will be validated and
    passed the the wrapped function.
    """
    method = request.method

    if method == 'PUT' or method == 'POST':
      try:
        data = codec.decode(request.data)
      except Exception, e:
        raise exc.BadRequest({'error': e.message})

      # TODO: this raises for now to see what this jam returns
      # Schema(schema).validate(data)

      return data

  @inject(instance=Instance, method_name=MethodName)
  def invoke(self, instance, method_name, request, args, kwargs):
    """
    Invoke the current resource's action, ensuring that all its required
    injected parameters are provided. Any extra parameters passed will be given
    to the function.
    """
    func = getattr(instance, method_name)

    injections = self._injector.args_to_inject(
      function  = func,
      bindings  = getattr(func, '__bindings__', {}),
      owner_key = func.__module__,
    )

    if request is None:
      return func(*args, **dict(injections, **kwargs))
    else:
      return func(request, *args, **dict(injections, **kwargs))
