import unittest

from rest.codec import JsonCodec


class TestCodec(unittest.TestCase):

  def setUp(self):
    self.json = JsonCodec()

  def test_echo(self):
    @self.json
    def echo(obj):
      return obj

    self.assertEquals('{"pants": 666}' , echo('{"pants":666}'))

  def test_simple_func(self):
    @self.json
    def double(i):
      return i * 2

    self.assertEquals('8', double('4'))
