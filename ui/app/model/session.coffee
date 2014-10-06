Backbone = require 'backbone'
inject   = require 'honk-di'

{Model}  = require './index'


class Session
  @scope: 'singleton'

  _url: ->
    @apiRoot + '/session'


module.exports = Session
