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

  def test_get_requet(self):
    resp = self.client.get('/test/simple-get')
    self.assert200(resp)
    self.assertEquals('{"simple": "object"}', resp.data)
