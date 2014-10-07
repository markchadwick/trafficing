ObserveModel = (fields...) ->

  componentDidMount: ->
    @_observe(field) for field in fields

  componentWillUnmount: ->
    @_unobserve(field) for field in fields

  _observe: (field) ->
    model = @props[field] or @state[field]
    model.on('add remove sync reset change',
      @forceUpdate.bind(this, null),
      this)

  _unobserve: (field) ->
    model = @props[field] or @state[field]
    model.off(null, null, this)

module.exports =
  ObserveModel: ObserveModel
