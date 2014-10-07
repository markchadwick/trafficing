/**
 * @jsx React.DOM
 */
'use strict';

var React = require('react');

var Label = React.createClass({displayName: 'Label',

  propTypes: {
    schema: React.PropTypes.object,
    label: React.PropTypes.string,
    hint: React.PropTypes.string
  },

  render: function() {
    var schema = this.props.schema;
    var label = this.props.label ? this.props.label : schema.props.label;
    var hint = this.props.hint ? this.props.hint : schema.props.hint;
    if (!hint && !label) {
      return React.DOM.span(null);
    }
    return this.transferPropsTo(
      React.DOM.label({className: "rf-Label"}, 
        label, 
        hint && Hint({hint: hint})
      )
    );
  }
});

var Hint = React.createClass({displayName: 'Hint',

  propTypes: {
    hint: React.PropTypes.string.isRequired
  },

  render: function() {
    return this.transferPropsTo(
      React.DOM.span({className: "rf-Hint"}, this.props.hint)
    );
  }
});

module.exports = Label;
