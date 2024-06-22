class DynamicFieldSerializerMixin(object):
    dynamic_fields: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, context_key in self.dynamic_fields.items():
            if not self.context.get(context_key):
                self.fields.pop(field_name, None)
