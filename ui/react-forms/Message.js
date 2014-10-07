/**
 * @jsx React.DOM
 */
'use strict';

var React = require('react');

var Message = React.createClass({displayName: 'Message',

  render: function() {
    return this.transferPropsTo(
      React.DOM.span({className: "rf-Message"}, 
        this.props.children
      )
    );
  }
});

module.exports = Message;
