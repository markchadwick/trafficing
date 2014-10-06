Backbone = require 'backbone'
Deferred = require 'deferred'
inject   = require 'honk-di'

Assets = require './assets'


# Backbone uses some supremely annoying global variables to make ajax requests.
# Instead, we'll bind it to a class to be set up in the bootstrap of either the
# application or tests.
class Ajax
  @scope: 'singleton'

  constructor: ->
    @ajax = @request.bind(this)

  _request: (options, deferred) ->
    throw new Error('Ajax._request is not implemented')

  request: (options) ->
    if not options? then throw new Error('You must provide options')
    deferred = Deferred()
    @_request(options, deferred)
    deferred.promise.then(options.success, options.error)


class XMLHttpAjax extends Ajax
  assets: inject Assets

  _request: (options, deferred) ->
    method = options.type or 'GET'
    url    = options.url

    download = @assets.track(url)
    xhr = new window.XMLHttpRequest()

    xhr.addEventListener 'progress', (e) ->
      download.progress(e.loaded, e.total)

    xhr.addEventListener 'load', ->
      download.finish()

    xhr.onload = (e) ->
      if @status is 200
        switch options.dataType
          when 'json' then deferred.resolve(JSON.parse(@response))
          else deferred.resolve(@response)
      else
        deferred.reject(e)

    xhr.open(method, url, true)
    xhr.send()

module.exports = {Ajax, XMLHttpAjax}
