_initDocument = ->
  domino = require 'domino'
  Window = require 'domino/lib/Window'

  global.document or= domino.createDocument()
  window = new Window(global.document)

  global.window     = window
  global.navigator  = window.navigator

  window


_destroyWindow = ->
  delete global.navigator
  delete global.window


# Initialize the window/document/navigator and add helpful functions for dealing
# with DOM elements.
beforeEach ->
  window  = _initDocument()

  React     = require('react')
  TestUtils = require('react/addons').addons.TestUtils

  @_nodes = []
  @render = (cls) ->
    el = document.createElement('div')
    @_nodes.push(el)
    document.body.appendChild(el)
    React.renderComponent(cls, el)

  @simulate   = TestUtils.Simulate
  @allByClass = TestUtils.scryRenderedComponentsWithClass
  @allByTag   = TestUtils.scryRenderedDOMComponentsWithTag
  @allByType  = TestUtils.scryRenderedComponentsWithType
  @oneByClass = TestUtils.findRenderedComponentWithClass
  @oneByTag   = TestUtils.findRenderedDOMComponentWithTag
  @oneByType  = TestUtils.findRenderedComponentWithType


# Nuke the global state of window/document/navigator
afterEach ->
  React = require('react')
  for node in @_nodes
    React.unmountComponentAtNode(node)

  _destroyWindow()


# if a 'window' is not in place when React first loads, it will silently get
# into a very bizarre state and throw an 'Invariant Violation' the first time
# you try to render something. This behavior seems specific to 0.10.0, so try
# removing this if you notice the currect React version is higher.
_initDocument()
