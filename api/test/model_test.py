from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject

from test import TestCase

class ModelTest(TestCase):

  @inject(db=SQLAlchemy)
  def setUp(self, db):
    super(ModelTest, self).setUp()
    from api import model

    db.drop_all()
    db.create_all()
    self.db = db
