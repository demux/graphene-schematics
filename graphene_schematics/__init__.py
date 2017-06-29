from collections import defaultdict

import graphene
from schematics.types import StringType, IntType, BooleanType, URLType, ListType, ModelType, DateTimeType


def _create_list_field(f):
    try:
        sub_field = make_class(f.field.model_class)
    except AttributeError:
        sub_field = type(_create_field(f.field))

    return graphene.List(sub_field)


# Map schematics field types to graphene field types:
field_type_map = {
    StringType: lambda f: graphene.String(),
    IntType: lambda f: graphene.Int(),
    BooleanType: lambda f: graphene.Boolean(),
    URLType: lambda f: graphene.String(),
    ListType: _create_list_field,
    ModelType: lambda f: graphene.Field(make_class(f.model_class)),
}

class _RegistryDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

registry = defaultdict(_RegistryDict)


_create_field = lambda f: field_type_map[type(f)](f)

def make_class(input_cls):
    class_name = input_cls.__name__
    input_module_name = input_cls.__module__

    # See first if this class already exists in the module registry:
    try:
        return registry[input_module_name][class_name]
    except KeyError:
        pass

    # Gather fields from schematics model and create graphene fields using field_type_map:
    fields = {name: _create_field(field) for name, field in input_cls._schema.fields.items()}

    # Create the new graphene class:
    cls = type(class_name, (graphene.ObjectType,), fields)

    # Register to module of origin to prevent dublicates:
    registry[input_module_name][class_name] = cls

    return cls


def make_classes(input_cls_list):
    for input_cls in input_cls_list:
        make_class(input_cls)

    return registry
