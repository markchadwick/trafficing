/**
 * @jsx React.DOM
 * @preventMunge
 */
'use strict';

var v = require('./validation');
var s = require('./schema');
var u = require('./utils');
var getDefaultValueForSchema = require('./getDefaultValueForSchema');



  function Value(parent, name, path, schema, value, serialized, validation) {
    this.parent = parent;
    this.name = name;
    this.path = path;
    this.schema = schema;
    this.value = value;
    this.serialized = serialized;
    this.validation = validation;

    this.isUndefined = this.value === undefined;

    if (this.value === undefined) {
      this.value = getDefaultValueForSchema(this.schema);
    }

    if (this.validation === undefined) {
      var validated = v.validate(this.schema, this.value);
      this.value = validated.value;
      this.validation = validated.validation;
    }

    if (this.serialized === undefined) {
      this.serialized = v.serialize(schema, this.value);
    }
  }

  Value.prototype.root=function() {
    var value = this;

    while (value.parent) {
      value = value.parent;
    }

    return value;
  };

  Value.prototype.forSchema=function(schema) {
    var root = this.root();
    // keep value and serialized value but drop validation state
    var newRoot = make(schema, root.value, root.serialized);
    return this.for_(newRoot);
  };

  Value.prototype.for_=function(root) {
    var value = root;

    for (var i = 0, len = this.path.length; i < len; i++) {
      value = value.get(this.path[i]);
    }

    return value;
  };

  Value.prototype.get=function(name) {
    return _make(
      this,
      name,
      this.path.concat(name),
      this.schema.get(name),
      this.value[name],
      this.serialized[name],
      (this.validation.children && this.validation.children[name]) || v.success
    );
  };

  Value.prototype.updateValue=function(value) {
    return this.update({value:value});
  };

  Value.prototype.updateValidation=function(validation) {
    return this.update({validation:validation});
  };

  Value.prototype.updateSerialized=function(serialized) {
    return this.update({serialized:serialized});
  };

  Value.prototype.update=function(update) {
    var current = this;
    update = this._updateSelf(update);

    while (current.parent) {
      update = current.parent._updateChild(current.name, update);
      current = current.parent;
    }

    return this.for_(make(
      current.schema,
      update.value,
      update.serialized,
      update.validation
    ));
  };

  Value.prototype._updateSelf=function(update) {
    u.invariant(
      !(update.value === undefined
        && update.serialized === undefined
        && update.validation === undefined)
    );

    if (update.value === undefined || update.validation === undefined) {
      var toValidate = update.value !== undefined ?
        update.value :
        update.serialized !== undefined ?
        update.serialized :
        this.value;
      var validated = v.validate(this.schema, toValidate);
      update.value = validated.value;
      update.validation = mergeValidation(
        validated.validation,
        update.validation);
    }

    if (update.serialized === undefined) {
      update.serialized = v.serialize(this.schema, update.value);
    }

    return update;
  };



function mergeValidation(a, b) {
  if (b === undefined || b === null) {
    return a;
  }

  var result = {
    validation: {},
    children: {}
  };

  if (b.validation) {
    result.validation = b.validation;
  } else if (a.validation) {
    result.validation = a.validation;
  }

  var k;

  if (b.children) {
    for (k in a.children) {
      result.children[k] = mergeValidation(a.children[k], b.children[k]);
    }

    for (k in b.children) {
      if (result.children[k] === undefined) {
        result.children[k] = b.children[k];
      }
    }
  } else {
    result.children = a.children;
  }

  return result;
}

for(var Value____Key in Value){if(Value.hasOwnProperty(Value____Key)){SchemaValue[Value____Key]=Value[Value____Key];}}var ____SuperProtoOfValue=Value===null?null:Value.prototype;SchemaValue.prototype=Object.create(____SuperProtoOfValue);SchemaValue.prototype.constructor=SchemaValue;SchemaValue.__superConstructor__=Value;function SchemaValue(){if(Value!==null){Value.apply(this,arguments);}}

  SchemaValue.prototype._updateChild=function(name, update) {
    update = this._updateSelf(update);

    var value = {};
    var serialized = {};
    var validation = {
      validation: this.validation.validation,
      children: {}
    };

    var n;

    for (n in this.value) {
      value[n] = this.value[n];
      serialized[n] = this.serialized[n];
    }

    for (n in this.validation.children) {
      validation.children[n] = this.validation.children[n];
    }

    value[name] = update.value;
    serialized[name] = update.serialized;
    validation.children[name] = update.validation;

    var validated = v.validateOnly(this.schema, value, validation.children);

    value = validated.value;
    validation = validated.validation;

    return {value:value, serialized:serialized, validation:validation};
  };


for(Value____Key in Value){if(Value.hasOwnProperty(Value____Key)){ListValue[Value____Key]=Value[Value____Key];}}ListValue.prototype=Object.create(____SuperProtoOfValue);ListValue.prototype.constructor=ListValue;ListValue.__superConstructor__=Value;function ListValue(){if(Value!==null){Value.apply(this,arguments);}}

  ListValue.prototype._updateChild=function(name, update) {
    update = this._updateSelf(update);

    var value = this.value.slice(0);
    var serialized = this.serialized.slice(0);

    var validation = {
      validation: this.validation.validation,
      children: {}
    };

    for (var n in this.validation.children) {
      validation.children[n] = this.validation.children[n];
    }

    value[name] = update.value;
    serialized[name] = update.serialized;
    validation.children[name] = update.validation;

    return {value:value, serialized:serialized, validation:validation};
  };

  ListValue.prototype.swap=function(aIndex, bIndex) {
    var value = this.value.slice(0);
    var serialized = this.serialized.slice(0);

    value.splice(bIndex, 0, value.splice(aIndex, 1)[0]);
    serialized.splice(bIndex, 0, serialized.splice(aIndex, 1)[0]);

    return this.update({value:value, serialized:serialized});
  };

  ListValue.prototype.add=function(value) {
    if (value === undefined) {
      value = getDefaultValueForSchema(this.schema.children);
    }

    return this.update({value: this.value.concat(value)});
  };

  ListValue.prototype.remove=function(index) {
    var value = this.value.slice(0);
    var serialized = this.serialized.slice(0);

    value.splice(index, 1);
    serialized.splice(index, 1);

    return this.update({value:value, serialized:serialized});
  };


for(Value____Key in Value){if(Value.hasOwnProperty(Value____Key)){PropertyValue[Value____Key]=Value[Value____Key];}}PropertyValue.prototype=Object.create(____SuperProtoOfValue);PropertyValue.prototype.constructor=PropertyValue;PropertyValue.__superConstructor__=Value;function PropertyValue(){if(Value!==null){Value.apply(this,arguments);}}



function _make(parent, name, path, schema, value, serialized, validation) {
  var constructor;
  if (s.isSchema(schema)) {
    constructor = SchemaValue;
  } else if (s.isList(schema)) {
    constructor = ListValue;
  } else if (s.isProperty(schema)) {
    constructor = PropertyValue;
  } else {
    u.invariant(false, 'invalid schema node');
  }

  return new constructor(
    parent, name, path, schema, value, serialized, validation);
}

function make(schema, value, serialized, validation) {
  return _make(null, null, [], schema, value, serialized, validation);
}

function isValue(value) {
  return value instanceof Value;
}

module.exports = make;
module.exports.isValue = isValue;
