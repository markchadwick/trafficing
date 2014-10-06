inject = require 'honk-di'

App           = require './app'
{Ajax}        = require './io/ajax'
{XMLHttpAjax} = require './io/ajax'


class Binder extends inject.Binder
  constructor: (@_config) ->
    super()

  configure: ->
    @bind(Ajax).to(XMLHttpAjax)
    @bindConstant('dom.root').to(document.body)

    for k, v of @_config
      @bindConstant(k).to(v)


init = (config) =>
  binder   = new Binder(config)
  injector = new inject.Injector(binder)
  app      = injector.getInstance(App)

  app.init()


window.trafficing = {init: init}
module.exports    = init
