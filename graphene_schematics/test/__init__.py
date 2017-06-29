import unittest

import graphene

import graphene_schematics

from . import models
from . import models2


class TestGrapheneSchematics(unittest.TestCase):
    def setUp(self):
        registry = graphene_schematics.make_classes([models.TestModel])
        self.schema = registry[models.__name__]
        self.schema2 = registry[models2.__name__]

    def test_generated_class_types(self):
        self.assertTrue(issubclass(self.schema.TestModel, graphene.ObjectType))
        self.assertTrue(issubclass(self.schema.TestModelChild, graphene.ObjectType))

        self.assertTrue(issubclass(self.schema2.TestModelOutside, graphene.ObjectType))

    def test_registry(self):
        self.assertEqual(len(graphene_schematics.registry), 2)

        # models.py
        models_registry = graphene_schematics.registry[models.__name__]
        self.assertEqual(len(models_registry), 2)
        self.assertEqual(models_registry.TestModel, self.schema.TestModel)
        self.assertEqual(models_registry.TestModelChild, self.schema.TestModelChild)

        # models2.py
        models2_registry = graphene_schematics.registry[models2.__name__]
        self.assertEqual(len(models2_registry), 1)
        self.assertEqual(models2_registry.TestModelOutside, self.schema2.TestModelOutside)

    def test_fields(self):
        fields = self.schema.TestModel._meta.fields

        self.assertEqual(fields['string']._type, graphene.String)
        self.assertEqual(fields['integer']._type, graphene.Int)
        self.assertEqual(fields['boolean']._type, graphene.Boolean)
        self.assertEqual(fields['url']._type, graphene.String)

        self.assertEqual(fields['model']._type, self.schema.TestModelChild)

        self.assertEqual(fields['outsider']._type, self.schema2.TestModelOutside)

        # List of strings:
        self.assertEqual(type(fields['lst']._type), graphene.List)
        self.assertEqual(fields['lst']._type._of_type, graphene.String)

        # List of models:
        self.assertEqual(type(fields['models']._type), graphene.List)
        self.assertEqual(fields['models']._type._of_type, self.schema.TestModelChild)


if __name__ == '__main__':
    unittest.main()
