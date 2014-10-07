/**
 * @jsx React.DOM
 */
'use strict';

var React       = require('react/addons');
var cx          = React.addons.classSet;
var FieldMixin  = require('./FieldMixin');
var Message     = require('./Message');
var Label       = require('./Label');
var isFailure   = require('./validation').isFailure;

/**
 * Field component represents values which correspond to Property schema nodes
 * and so received PropetyValue as value.
 *
 * It provides basic markup which include <input /> component (can be customized
 * via schema) and <label /> (label text and hint text).
 */
var Field = React.createClass({displayName: 'Field',
  mixins: [FieldMixin],

  propTypes: {
    label: React.PropTypes.string
  },

  render: function() {
    var value = this.value();
    var externalValidation = this.externalValidation();
    var isInvalid = isFailure(value.validation)
                 || isFailure(externalValidation.validation);

    var className = cx({
      'rf-Field': true,
      'rf-Field--invalid': isInvalid,
      'rf-Field--dirty': !value.isUndefined
    });

    var id = this._rootNodeID;

    var input = this.renderInputComponent({id:id, onBlur: this.onBlur});

    return (
      React.DOM.div({className: cx(className, this.props.className)}, 
        this.renderLabel(id), 
        this.transferPropsTo(input), 
        isFailure(externalValidation) &&
          Message(null, externalValidation.validation.failure), 
        isFailure(value.validation) && !value.isUndefined &&
          Message(null, value.validation.validation.failure)
      )
    );
  },

  renderLabel: function(htmlFor) {
    var schema = this.value().schema;
    return (
      Label({
        htmlFor: htmlFor, 
        className: "rf-Field__label", 
        schema: schema, 
        label: this.props.label, 
        hint: this.props.hint}
        )
    );
  },

  onBlur: function() {
    var value = this.value();
    if (value.isUndefined) {
      this.onValueUpdate(value.update({value: value.value}));
    }
  }
});

module.exports = Field;
