from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase


# https://medium.com/@mohammedhammoud/aeb8b3c8fc4a
class AbstractModelTestCase(TestCase):
    abstract_model = None
    derived_model = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.derived_model = ModelBase(
            "TestModel" + cls.abstract_model.__name__,
            (cls.abstract_model,),
            {"__module__": cls.abstract_model.__module__},
        )

        with connection.schema_editor() as editor:
            editor.create_model(cls.derived_model)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        with connection.schema_editor() as editor:
            editor.delete_model(cls.derived_model)

        connection.close()
