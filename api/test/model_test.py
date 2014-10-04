from api import model
from test import TestCase


class ModelTest(TestCase):

  def setUp(self):
    super(ModelTest, self).setUp()

    model.db.drop_all()
    model.db.create_all()
