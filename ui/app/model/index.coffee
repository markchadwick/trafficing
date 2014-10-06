Backbone  = require 'backbone'
inject    = require 'honk-di'


class Model extends Backbone.Model


class Collection extends Backbone.Collection
  apiRoot:    inject 'api.root'

  apiUrl: (path) ->
    @rootUrl + path

  constructor: ->
    super
    @fetch(reset: true)


module.exports = {Collection, Model}
