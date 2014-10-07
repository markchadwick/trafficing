inject = require 'honk-di'


injector = undefined


Injected =
  inject: ->
    injector.getInstance(arguments...)


module.exports =
  Injected: Injected
  setMixinInjector: (i) -> injector = i
