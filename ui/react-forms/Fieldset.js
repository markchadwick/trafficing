/**
 * @jsx React.DOM
 */
'use strict';

var React         = require('react/addons');
var cx            = React.addons.classSet;
var Label         = require('./Label');
var FieldsetMixin = require('./FieldsetMixin');

/**
 * A component which renders a set of fields.
 *
 * It is used by <Form /> component at top level to render its fields.
 */
var Fieldset = React.createClass({displayName: 'Fieldset',
  mixins: [FieldsetMixin],

  render: function() {
    var schema = this.value().schema;
    return this.transferPropsTo(
      React.DOM.div({className: cx("rf-Fieldset", this.props.className)}, 
        this.renderLabel(), 
        schema.map(this.renderField)
      )
    );
  },

  renderLabel: function() {
    var schema = this.value().schema;
    return (
      Label({
        className: "rf-Fieldset__label", 
        schema: schema, 
        label: this.props.label, 
        hint: this.props.hint}
        )
    );
  }
});

module.exports = Fieldset;
