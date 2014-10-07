SetInterval =
  componentWillMount: ->
    @_intervals = []

  componentWillUnmount: ->
    @_intervals.map(clearInterval)

  setInterval: ->
    @_intervals.push(setInterval.apply(null, arguments))

module.exports =
  SetInterval: SetInterval
