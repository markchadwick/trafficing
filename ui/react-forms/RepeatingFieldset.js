/**
 * @jsx React.DOM
 */
'use strict';

var React                   = require('react/addons');
var cx                      = React.addons.classSet;
var Label                   = require('./Label');
var RepeatingFieldsetMixin  = require('./RepeatingFieldsetMixin');

var Item = React.createClass({displayName: 'Item',

  render: function() {
    return this.transferPropsTo(
      React.DOM.div({className: "rf-RepeatingFieldset__item"}, 
        this.props.children, 
        React.DOM.button({
          onClick: this.onRemove, 
          type: "button", 
          className: "rf-RepeatingFieldset__remove"}, "×")
      )
    );
  },

  onRemove: function() {
    if (this.props.onRemove) {
      this.props.onRemove(this.props.name);
    }
  }

});

/**
 * A component which renders values which correspond to List schema node.
 */
var RepeatingFieldset = React.createClass({displayName: 'RepeatingFieldset',

  mixins: [RepeatingFieldsetMixin],

  getDefaultProps: function() {
    return {
      item: Item
    };
  },

  render: function() {
    var Component = this.props.item;
    var fields = this.renderFields().map(function(item) 
      {return Component({
        key: item.props.name, 
        name: item.props.name, 
        onRemove: this.remove}, 
        item
      );}.bind(this)
    );
    return this.transferPropsTo(
      React.DOM.div({className: cx("rf-RepeatingFieldset", this.props.className)}, 
        this.renderLabel(), 
        fields, 
        React.DOM.button({
          type: "button", 
          onClick: this.onAdd, 
          className: "rf-RepeatingFieldset__add"}, "Add")
      )
    );
  },

  renderLabel: function() {
    var schema = this.value().schema;
    return (
      Label({
        className: "rf-RepeatingFieldset__label", 
        schema: schema, 
        label: this.props.label, 
        hint: this.props.hint}
        )
    );
  },

  onAdd: function () {
    this.add();
  }

});

module.exports = RepeatingFieldset;
module.exports.Item = Item;
