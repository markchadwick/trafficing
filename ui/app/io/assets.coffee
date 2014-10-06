Backbone = require 'backbone'


# Keep track of loading assets
class Assets extends Backbone.Model
  @scope: 'singleton'

  constructor: ->
    @_downloads = {}

  track: (url) ->
    download = new Download(url, this)
    @_downloads[url] = download
    download

  status: ->
    loaded  = 0
    total   = 0
    pending = 0

    for url, download of @_downloads
      pending += 1
      loaded  += download.loaded
      total   += download.total

    loaded:   loaded
    total:    total
    pending:  pending

  finish: (url) ->
    delete @_downloads[url]


class Download
  constructor: (@url, @assets) ->
    @loaded   = 0
    @total    = 1
    @assets.trigger('change')

  progress: (@loaded, @total) =>
    @assets.trigger('change')

  finish: =>
    @assets.finish(@url)
    @assets.trigger('change')

  fail: =>
    @assets.finish(@url)
    @assets.trigger('change')

module.exports = Assets
