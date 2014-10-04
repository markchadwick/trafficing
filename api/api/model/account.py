from sqlalchemy import Column
from sqlalchemy import String

from api.model import Base
from api.model import WithPublicId


class Account(Base, WithPublicId):
  __tablename__ = 'users'

  email = Column(String(255), nullable=False, unique=True)
  name  = Column(String(255), nullable=False)
