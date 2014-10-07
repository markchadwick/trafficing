/**
 * @jsx React.DOM
 */
'use strict';

var React = require('react');

function renderEmptyOption(props, onChange) {
  return (
    React.DOM.div({
        className: "rf-RadioButtonGroup__button", 
        key: ""}, 
      React.DOM.label({
        className: "rf-RadioButtonGroup__label"}, 
        React.DOM.input({
          checked: props.checked, 
          className: "rf-RadioButtonGroup__radio", 
          type: "radio", 
          name: props.name, 
          onChange: onChange.bind(null, null), 
          value: ""}), 
        React.DOM.span({className: "rf-RadioButtonGroup__caption"}, 
          "none"
        )
      )
    )
  );
}

var RadioButtonGroup = React.createClass({displayName: 'RadioButtonGroup',

    propTypes: {
      options: React.PropTypes.array.isRequired,
      allowEmpty: React.PropTypes.bool,
      value: React.PropTypes.string,
      onChange: React.PropTypes.func
    },

    render: function() {
      var options = this.props.options.map(this.renderOption);

      if (this.props.allowEmpty) {
        options.unshift(renderEmptyOption({
            name: this._rootNodeID,
            checked: !this.props.value
        }, this.onChange));
      }

      return (
        React.DOM.div({className: "rf-RadioButtonGroup"}, 
          options
        )
      );
    },

    renderOption: function(option) {
      var name = this._rootNodeID;
      var checked = this.props.value ?
          this.props.value === option.value :
          false;
      return (
        React.DOM.div({
          className: "rf-RadioButtonGroup__button", 
          key: option.value}, 
          React.DOM.label({
            className: "rf-RadioButtonGroup__label"}, 
            React.DOM.input({
              checked: checked, 
              className: "rf-RadioButtonGroup__radio", 
              type: "radio", 
              name: name, 
              onChange: this.onChange.bind(null, option.value), 
              value: option.value}), 
            React.DOM.span({className: "rf-RadioButtonGroup__caption"}, 
              option.name
            )
          )
        )
      );
    },

    onChange: function(value) {
      if (this.props.onChange) {
        this.props.onChange(value);
      }
    }
});

module.exports = RadioButtonGroup;
