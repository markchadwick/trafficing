import unittest

from injector import Injector
from injector import inject


class Pants(object):

  @inject(name=str)
  def say(self, name):
    return 'hi %s' % (name)


class TestInjector(unittest.TestCase):

  def test_call_injection(self):
    def configure(binder):
      binder.bind(str, to='Steve')
    injector = Injector(configure)
    pants = injector.get(Pants)

    self.assertEquals('hi Steve', pants.say())

  def test_method_bindings(self):
    pants = Pants()
    self.assertEquals({'name': (str,)}, pants.say.__bindings__)
