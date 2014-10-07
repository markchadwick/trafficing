React      = require 'react'
ReactForms = require '../../react-forms'

Form     = ReactForms.Form
Property = ReactForms.schema.Property
Schema   = ReactForms.schema.Schema


LoginView = React.createClass
  propTypes:
    onSubmit: React.PropTypes.func
    pending:  React.PropTypes.bool

  getDefaultProps: ->
    pending: false

  handleChange: (value, update) ->
    @email    = value.email
    @password = value.password
    @props.onChange?(value)

  handleSubmit: (e) ->
    e.preventDefault()
    @props.onSubmit?(@email, @password)

  componentWillMount: ->
    @email    = ''
    @password = ''

  render: ->
    <LoginView.Form
        disabled = {not @props.pending}
        schema   = LoginView.Schema
        onUpdate = @handleChange
        onSubmit = @handleSubmit />

LoginView.Schema =
  <Schema>
    <Property name='email' label='Email' />
    <Property name='password' label='Password' />
  </Schema>

LoginView.Form = React.createClass

  propTypes:
    onSubmit: React.PropTypes.func
    disabled:  React.PropTypes.bool

  onSubmit: ->
    @props.onSubmit?(arguments...)

  render: ->
    form = @transferPropsTo(<Form ref="form" component={React.DOM.div} />)
    <form onSubmit=@onSubmit>
      {form}
      <button type='submit' disabled=@props.disabled>
        Log In
      </button>
    </form>


module.exports = LoginView
