require './test_dom'
require './test_injected'

require('chai').use(require('./matchers'))

{Ajax} = require '../app/io/ajax'


beforeEach ->
  @req = @injector.getInstance(Ajax)
