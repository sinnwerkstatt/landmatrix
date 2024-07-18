from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase


# https://medium.com/@mohammedhammoud/aeb8b3c8fc4a
class AbstractModelMixinTestCase(TestCase):
    mixin = None
    model = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = ModelBase(
            "TestModel" + cls.mixin.__name__,
            (cls.mixin,),
            {"__module__": cls.mixin.__module__},
        )

        with connection.schema_editor() as editor:
            editor.create_model(cls.model)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        with connection.schema_editor() as editor:
            editor.delete_model(cls.model)

        connection.close()
