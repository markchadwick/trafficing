from os import path


def abs(name):
  pwd = path.dirname(path.realpath(__file__))
  return path.join(pwd, name)
