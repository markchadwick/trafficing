React     = require 'react'
inject    = require 'honk-di'

Session = require './model/session'
{Ajax}  = require './io/ajax'

AppController = require './controller/app_controller'


class App
  el: inject 'dom.root'

  init: ->
    React.renderComponent(<AppController />, @el)

    this


module.exports = App
