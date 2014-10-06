import functools

from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector

from api.module import ApiV1Module
from api.module import AppModule
from api.module import DbModule


def app_and_injector(config_file, *ext_mods):
  parent  = Injector([AppModule(config_file)])
  app     = parent.get(Flask)
  modules = [
    DbModule(app),
    ApiV1Module(app),
  ]

  i = FlaskInjector(app, modules + list(ext_mods), parent)
  return i.app, i.injector


def update_wrapper(wrapper, wrapped, assigned, updated):
  for attr in assigned:
    setattr(wrapper, attr, getattr(wrapped, attr))
  for attr in updated:
    getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

  wrapper_bindings = getattr(wrapper, '__bindings__', {})
  wrapped_bindings = getattr(wrapped, '__bindings__', None)
  if wrapped_bindings is not None:
    wrapper_bindings.update(wrapped_bindings)
    # delattr(wrapped, '__bindings__')
    setattr(wrapper, '__bindings__', wrapper_bindings)

  return wrapper

def wraps(func):
  """
  The defaufault behavior of function wrapping causes all kinds of problems with
  the injection decorator. Long story short, it updates the __dict__ by default,
  so wrapped bindings are lost. Instead, use the custom update_wrapper which
  will copy the wrapped __bindings__ to the wrapper.
  """
  return functools.partial(update_wrapper, wrapped=func,
    assigned=functools.WRAPPER_ASSIGNMENTS,
    updated={})


def combine_injection(decorator, wrapped, *args, **kwargs):
  wrapper = decorator(wrapped, *args, **kwargs)

  wrapper_bindings = getattr(wrapper, '__bindings__', {})
  wrapped_bindings = getattr(wrapped, '__bindings__', {})

  def call(*args, **kwargs):
    pass



  # Give the new function the superset of bindings along with the name doc etc
  # of the wrapped function
  functools.update_wrapper(call, wrapped)
  bindings = wrapper_bindings.copy()
  bindings.update(wrapped_bindings)
  call.__bindings__ = bindings

  return call
