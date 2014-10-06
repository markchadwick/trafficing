import unittest

from injector import Injector
from injector import inject

from api import wraps


def with_age(func):

  @wraps(func)
  @inject(age=int)
  def age_wrapper(*args, **kwargs):
    print '- ' * 30
    print 'args', args
    print 'kwargs', kwargs
    print '- ' * 30
    return func(*args, **kwargs)
  return age_wrapper

class Pants(object):

  @inject(name=str)
  def say(self, name):
    return 'hi %s' % (name)

  @with_age
  @inject(name=str)
  def name_and_age(self, name, age):
    return '%s is %d' % (name, age)


class TestInjector(unittest.TestCase):

  # def test_call_injection(self):
  #   def configure(binder):
  #     binder.bind(str, to='Steve')
  #   injector = Injector(configure)
  #   pants = injector.get(Pants)

  #   self.assertEquals('hi Steve', pants.say())

  # def test_method_bindings(self):
  #   pants = Pants()
  #   self.assertEquals({'name': (str,)}, pants.say.__bindings__)

  # def test_decorator_bindings(self):
  #   f = with_age(lambda d: d + 1)
  #   self.assertEquals({'age': (int,)}, f.__bindings__)

  def test_nested_bindings(self):
    @inject(name=str)
    def say(name, age):
      return '%s is %s' % (name, age)
    func = with_age(say)
    self.assertEquals({'age': (int,), 'name': (str,)}, func.__bindings__)

  def test_nested_methods(self):
    def configure(binder):
      binder.bind(str, to='Jimmy')
      binder.bind(int, to=100)
    pants = Injector(configure).get(Pants)

    self.assertEquals({'age': (int,), 'name': (str,)},
                      pants.name_and_age.__bindings__)

    self.assertEquals('Jimmy is 100', pants.name_and_age())
