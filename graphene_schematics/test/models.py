from schematics.models import Model
from schematics.types import StringType, IntType, BooleanType, URLType, ListType, ModelType

from .models2 import TestModelOutside


class TestModelChild(Model):
    pass


class TestModel(Model):
    string = StringType()
    integer = IntType()
    boolean = BooleanType()
    url = URLType()
    lst = ListType(StringType)

    model = ModelType(TestModelChild)

    models = ListType(ModelType(TestModelChild))

    outsider = ModelType(TestModelOutside)
