
class Collection(object):
  def __init__(self, model, db):
    self._model = model
    self._db = db

    self.query = db.session.query(model)
