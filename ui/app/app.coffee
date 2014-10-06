Backbone  = require 'backbone'
React     = require 'react'
inject    = require 'honk-di'

Session = require './model/session'
{Ajax}  = require './io/ajax'

# LoginController = require './controller/login_controller'


class App
  @scope: 'singleton'

  ajax: inject Ajax
  el:   inject 'dom.root'

  init: ->
    Backbone.ajax = @ajax.ajax

module.exports = App
