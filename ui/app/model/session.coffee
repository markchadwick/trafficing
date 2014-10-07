Backbone = require 'backbone'
inject   = require 'honk-di'

{Ajax}   = require '../io/ajax'
{Model}  = require './index'


class Session extends Model
  @scope: 'singleton'

  apiRoot:  inject 'api.root'
  ajax:     inject Ajax

  constructor: ->
    @url = @apiRoot + '/session'
    super



module.exports = Session
