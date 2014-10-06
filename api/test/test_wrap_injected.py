import unittest

from injector import Injector
from injector import Key
from injector import inject

from api import combine_injection

Age  = Key('age')
Name = Key('name')


def with_age(func):
  @inject(age=Age)
  def age_wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return age_wrapper

def with_name(func):
  @inject(name=Name)
  def name_wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return name_wrapper

def say_age(age):
  return 'age is %d' % (age)


class TestWrapInjected(unittest.TestCase):
  def setUp(self):
    def configure(binder):
      binder.bind(Age, to=666)
      binder.bind(Name, to='Frank')
    self.injector = Injector()

  def test_simple_function_bindings(self):
    func = combine_injection(with_age, say_age)
    self.assertEquals('say_age', func.__name__)
    self.assertEquals({'age': (Age,)}, func.__bindings__)

  def test_combined_function_bindings(self):
    decorator = combine_injection(with_age, with_name)
    func      = combine_injection(decorator, say_age)
    bindings  = func.__bindings__

    self.assertEquals({'age': (Age,), 'name': (Name,)}, bindings)
