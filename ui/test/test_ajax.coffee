{Ajax} = require '../app/io/ajax'


class TestAjax extends Ajax

  constructor: ->
    super
    @_handlers = []

  _request: (options, deferred) ->
    for [match, handler] in @_handlers
      match = true
      for k, v of match
        if options[k] isnt v
          match = false
          continue
      if match
        handler(options, deferred.resolve, deferred.reject)
      else
        message "#{options.type} #{options.url} not found"
        deferred.reject(status: 404, message: message)

  match: (match, handler) ->
    @_handlers.push([match, handler])


module.exports = TestAjax
