React = require 'react'

LoginController = require './login_controller'

Session    = require '../model/session'
{Injected} = require '../mixin'


AppController = React.createClass
  mixins: [Injected]

  getInitialState: ->
    session:        @inject Session
    sessionLoaded:  false
    loggedIn:       false

  loadSession: ->
    @state.session.fetch
      success: => @setState(sessionLoaded: true, loggedIn: true)
      error:   => @setState(sessionLoaded: true, loggedIn: false)

  loggedIn: ->
    console.log "we're logged in!"

  render: ->
    if not @state.sessionLoaded
      console.log 'rendering loader'
      @loadSession()
      return <span>...</span>

    if not @state.loggedIn
      console.log 'rendering login controller'
      return <LoginController onComplete=@loggedIn />

    console.log 'rendering app'
    return <h1>App1!</h1>


module.exports = AppController
