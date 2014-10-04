from base64 import urlsafe_b64encode
from sqlalchemy import Column
from sqlalchemy import String
from uuid import uuid4


def new_id():
  """
  Create a new unique identifier that is safe for URLs and public identifiers --
  ie: it could not be guessed, and is safe to put as part of a path in URL
  without worrying about escaping.
  """
  bs = uuid4().bytes
  return urlsafe_b64encode(bs).strip().replace('=', '')


class WithPublicId(object):
  """
  Gives the model a URL-safe an likely un-guessable ID field. Each model that
  mixes in this class will grow an "id" field of VARCHAR(22)
  """
  id = Column(String(22), default=new_id, primary_key=True)

  def is_new(self):
    return not self.id
