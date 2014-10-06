from flask import Flask
from flask_injector import request
from injector import Module
from injector import inject
from schema import And
from schema import Use

from rest import JsonCodec
from rest import Resource
from rest import Resources
from test import TestCase


@request
class NoOp(object): pass


@request
class SimpleGet(object):
  name = 'simple'

  def get(self):
    return {'simple': 'object'}

@request
class WithSchema(object):
  name = 'with-scheama'

  schema = {
    'name':   And(str, len),
    'age':    Use(int),
  }

  def create(self, person):
    return person


class Request(object):
  def __init__(self, method, data=None):
    self.method = method
    self.data = data


class RoutingModule(Module):
  @inject(app=Flask)
  def configure(self, binder, app):
    resources = Resources('test', [
      ('/noop',         NoOp),
      ('/simple-get',   SimpleGet),
      ('/with-schema',  WithSchema),
    ])
    resources.bind(app, '/test')


class TestResource(TestCase):

  def modules(self):
    return [RoutingModule()]

  def test_parse_get_request(self):
    self.called = False
    def handle():
      self.called = True

    noop    = Resource(NoOp, 'noop')
    request = Request('GET')
    codec   = JsonCodec()
    wrapped = noop._parse_request(handle)

    wrapped(request=request, codec=codec)
    self.assertTrue(self.called)

  def test_parse_post(self):
    self.called = False
    def handle(data):
      self.assertEquals({'hi': [123]}, data)
      self.called = True

    noop    = Resource(NoOp, 'noop')
    request = Request('POST', '{"hi":[123]}')
    codec   = JsonCodec()
    wrapped = noop._parse_request(handle)

    wrapped(request=request, codec=codec)
    self.assertTrue(self.called)

  def test_get_requet(self):
    resp = self.client.get('/test/simple-get')
    self.assert200(resp)
    self.assertEquals('{"simple": "object"}', resp.data)

  # def test_post_with_schema(self):
  #   resp = self.client.post('/test/with-schema/')
  #   print '- ' * 30
  #   print resp
  #   print resp.data
  #   print '- ' * 30
  #   self.assert200(resp)
  #   self.assertEquals('{"simple": "object"}', resp.data)
