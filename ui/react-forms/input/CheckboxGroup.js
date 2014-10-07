/**
 * @jsx React.DOM
 */
'use strict';

var React = require('react');

var CheckboxGroup = React.createClass({displayName: 'CheckboxGroup',

  propTypes: {
    options: React.PropTypes.array.isRequired,
    value: React.PropTypes.array,
    onChange: React.PropTypes.func
  },

  getDefaultProps: function() {
    return {value: []};
  },

  onChange: function(e) {
    if (!this.props.onChange) {
      return;
    }

    var nextValue = this.props.value.slice(0);

    if (e.target.checked) {
      nextValue.push(e.target.value);
    } else {
      var idx = nextValue.indexOf(e.target.value);
      if (idx > -1) {
        nextValue.splice(idx, 1);
      }
    }

    var values = this.props.options.map(function(o)  {return o.value;});
    nextValue.sort(function(a, b)  {return values.indexOf(a) - values.indexOf(b);});

    this.props.onChange(nextValue);
  },

  render: function() {
    var name = this._rootNodeID;
    var value = this.props.value;
    var options = this.props.options.map(function(option)  {
      var checked = value && value.indexOf(option.value) > -1;
      return (
        React.DOM.div({
          className: "rf-CheckboxGroup__button", 
          key: option.value}, 
          React.DOM.label({className: "rf-CheckboxGroup__label"}, 
            React.DOM.input({
              onChange: this.onChange, 
              checked: checked, 
              className: "rf-CheckboxGroup__checkbox", 
              type: "checkbox", 
              name: name, 
              value: option.value}), 
            React.DOM.span({className: "rf-CheckboxGroup__caption"}, 
              option.name
            )
          )
        )
      );
    }.bind(this));

    return (
      React.DOM.div({className: "rf-CheckboxGroup"}, 
        options
      )
    );
  }
});

module.exports = CheckboxGroup;
