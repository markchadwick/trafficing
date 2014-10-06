import json
import unittest

from functools import partial
from injector import Injector
from nose.exc import SkipTest
from nose.tools import raises

from rest import exc
from rest.codec import JsonCodec
from rest.handler import Handler


class Request(object):
  def __init__(self, method, data=None):
    self.method = method
    self.data = data

class TestHandler(unittest.TestCase):
  def setUp(self):
    def configure(binder):
      pass

    self.injector = Injector(configure)
    self.handler  = Handler(self.injector)

    self.request = partial(self.handler.request,
      codec  = JsonCodec(),
      schema = {})

  def test_parse_get_request(self):
    request = Request('GET')
    req = self.request(request)
    self.assertTrue(req is None)

  def test_post_request(self):
    payload = {'hi': [123]}
    request = Request('POST', json.dumps(payload))
    self.assertEquals(payload, self.request(request))

  @raises(exc.BadRequest)
  def test_bad_post_request(self):
    request = Request('POST', 'what?')
    self.request(request)

  def test_bad_request_schema(self):
    raise SkipTest()
    request = Request('POST', '22')
    self.request(request)

  def return_42(self): return 42
  def test_simple_invoke(self):
    result = self.handler.invoke(
      instance    = self,
      method_name = 'return_42',
      request     = None,
      args   = [],
      kwargs = {})
    self.assertEquals(42, result)

  def echo(self, body): return body
  def test_request_invoke(self):
    result = self.handler.invoke(
      instance    = self,
      method_name = 'echo',
      request     = 'Woah, request!',
      args   = [],
      kwargs = {})

    self.assertEquals('Woah, request!', result)
