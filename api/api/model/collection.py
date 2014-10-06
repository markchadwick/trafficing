
class Collection(object):
  _query_fields = [
    'filter',
    'filter_by',
    'get',
  ]

  def __init__(self, model, db):
    self._model = model
    self._db = db
    query = db.session.query(model)
    self.query = query

    for field in Collection._query_fields:
      setattr(self, field, getattr(query, field))
