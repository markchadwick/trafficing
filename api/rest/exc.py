class RestException(Exception):
  def __init__(self, status, message=''):
    self.status  = status
    self.message = message
    super(RestException, self).__init__(message)

  def toObject(self):
    return {
      'error': self.message
    }


class BadRequest(RestException):
  def __init__(self, errors):
    super(BadRequest, self).__init__(400, 'Bad Request')
    self.errors = errors

  def toObject(self):
    return self.errors


class Forbidden(RestException):
  def __init__(self, message=None):
    if message is None:
      message = '403 Forbidden'
    super(Forbidden, self).__init__(403, message)


class InternalServerError(RestException):
  def __init__(self, message=None):
    super(Forbidden, self).__init__(500, 'Internal Server Error')
