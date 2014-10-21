
def schema_interceptor(schema, update, chain):
  in_model = schema(update)
  in_model.validate()

  out_model = chain(in_model)
  return out_model.to_primitive()
