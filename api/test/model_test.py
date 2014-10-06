from abc import ABCMeta
from abc import abstractmethod
from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject
from injector import Module

from api import model
from test import TestCase


class SchemaStrategy(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def setup(self): pass

  @abstractmethod
  def teardown(self): pass


class ModelTest(TestCase):

  class ModelModule(Module):
    def configure(self, binder):
      binder.bind(SchemaStrategy, RebuildSchema)

  def modules(self):
    return [ModelTest.ModelModule()]

  @inject(db=SQLAlchemy, schema=SchemaStrategy)
  def setUp(self, db, schema):
    super(ModelTest, self).setUp()

    self.db = db
    self.session = db.session

    schema.setup()

  @inject(schema=SchemaStrategy)
  def tearDown(self, schema):
    schema.teardown()
    super(ModelTest, self).tearDown()

  def echo_on(self):
    engine = self.db.engine
    class with_echo_on(object):
      def __enter__(self):
        engine.echo = True
      def __exit__(self, type, value, traceback):
        engine.echo = False
    return with_echo_on()


class RebuildSchema(SchemaStrategy):

  @inject(db=SQLAlchemy)
  def __init__(self, db):
    self.db = db

  def setup(self):
    self.db.drop_all()
    self.db.create_all()

  def teardown(self):
    pass


class TransactionSchema(SchemaStrategy):

  @inject(db=SQLAlchemy)
  def __init__(self, db):
    db.create_all()
    self.db = db

  def setup(self):
    self.db.session.begin(subtransactions=True)

  def teardown(self):
    self.db.session.rollback()
    self.db.session.close()
