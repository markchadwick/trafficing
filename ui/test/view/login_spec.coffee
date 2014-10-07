require '../test_case'

LoginView = require '../../app/view/login'


describe 'Login View', ->

  it 'render with no default values', ->
    view = @render <LoginView />
    console.log '------------------------------------'
    console.log view.getDOMNode().innerHTML
    console.log '------------------------------------'
