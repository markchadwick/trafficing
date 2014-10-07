inject = require 'honk-di'

{Ajax}   = require '../app/io/ajax'
TestAjax = require './test_ajax'

{setMixinInjector} = require '../app/mixin/injected'


class Binder extends inject.Binder
  configure: ->
    @bind(Ajax).to(TestAjax)
    @bindConstant('api.root').to('/')


beforeEach ->
  @binder   = new Binder()
  @injector = new inject.Injector(@binder)
  setMixinInjector(@injector)


module.exports = Binder
