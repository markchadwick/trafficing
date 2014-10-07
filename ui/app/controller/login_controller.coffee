React      = require 'react'
ReactForms = require '../../react-forms'

Schema   = ReactForms.schema.Schema
Property = ReactForms.schema.Property
Form     = ReactForms.Form

Session    = require '../model/session'
{Injected} = require '../mixin'

LoginView = require '../view/login'

LoginSchema =
  <Schema>
    <Property name='email' label='Email' />
    <Property name='password' label='Password' />
  </Schema>



LoginController = React.createClass
  mixins: [Injected]

  propTypes:
    onComplete: React.PropTypes.func

  getInitialState: ->
    session:  @inject Session
    loggedIn: false
    pending:  true

  handleSubmit: (update) ->
    @setState(pending: true)
    @state.session.save(update, {
      method: 'PUT'
      success: => @setState(pending: false, loggedIn: true)
      error:   => @setState(pending: false, loggedIn: false)
    })

  render: ->
    <LoginView pending=@state.pending onSubmit=@handleSubmit />


module.exports = LoginController
