React      = require 'react'
ReactForms = require 'react-forms'

Session    = require '../model/session'
{Injected} = require '../mixin'


Schema   = ReactForms.schema.Schema
Property = ReactForms.schema.Property
Form = ReactForms.Form

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

  handleChange: (update) ->
    console.log 'update', update
    @state.session.set(update)
    console.log 'json', @state.session.toJSON()

  render: ->
    <div>
      <Form schema=LoginSchema onUpdate=@handleChange />
    </div>


module.exports = LoginController
