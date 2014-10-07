React      = require 'react'
ReactForms = require '../../react-forms'

Form     = ReactForms.Form
Property = ReactForms.schema.Property
Schema   = ReactForms.schema.Schema


LoginView = React.createClass
  propTypes:
    onChange: React.PropTypes.func

  handleChange: (value, update) ->
    @email    = value.email
    @password = value.password

    @props.onChange?(value)

  componentWillMount: ->
    @email    = ''
    @password = ''

  render: ->
    <div>
      <Form schema=LoginView.Schema onUpdate=@handleChange />
    </div>


LoginView.Schema =
  <Schema>
    <Property name='email' label='Email' />
    <Property name='password' label='Password' />
  </Schema>

module.exports = LoginView
