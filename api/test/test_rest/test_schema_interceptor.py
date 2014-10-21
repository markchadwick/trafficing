import unittest

from schematics.models import Model
from schematics.types import StringType

from rest.schema_interceptor import schema_interceptor


class Person(Model):
  name = StringType(required=True)


class TestSchemaInterceptor(unittest.TestCase):

  def test_basic_call(self):
    self.called = False
    def process(person):
      self.assertEquals('Bill', person.name)
      self.called = True
      person.name += '!!'
      return person

    result = schema_interceptor(Person, {'name': 'Bill'}, process)
    self.assertTrue(self.called)
    self.assertEquals('Bill!!', result['name'])

  def test_invaid_schema(self):
    schema_interceptor(Person, {}, None)
