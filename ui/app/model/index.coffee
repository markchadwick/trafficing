Backbone  = require 'backbone'
inject    = require 'honk-di'


class Model extends Backbone.Model


class Collection extends Backbone.Collection
  apiRoot:    inject 'api.root'

  apiUrl: (path) ->
    @rootUrl + path


module.exports = {Collection, Model}
