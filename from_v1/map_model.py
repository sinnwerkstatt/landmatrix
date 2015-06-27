__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from migrate import V1, V2

from django.db import models, transaction

"""
    Map a model from Landmatrix V1 to Landmatrix V2.
    Usage:
    - Subclass MapModel
    - set the class variables old_class and new_class to the models in V1 and V2
    - optionally:
      - set the class variable depends to a list of mappings that need to be run before this
      - set the class variable attributes to a dict of mappings of old attribute names to new attribute names
      - optionally, the second parameter of the mapping can be a pir of (new_attribute_name, processing_function)
    - run map_all() (or map() to convert a single record)

    Example:

        def year_to_date(year):
            return None if year is None else str(year)+'-01-07'

        class MapActivityAttributeGroup(MapModel):
            old_class = editor.models.ActivityAttributeGroup
            new_class = landmatrix.models.ActivityAttributeGroup
            attributes = {
                'activity': 'fk_activity',
                'language': 'fk_language',
                'year': ('date', year_to_date)
            }
            depends = [ MapActivity, MapLanguage ]

"""
class MapModel:

    attributes = { }
    depends = []

    @classmethod
    def map(cls, id, save=False):
        record = cls.old_class.objects.using(V1).filter(id=id).values()[0]
        cls.map_record(record, save)

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False):

        cls._check_dependencies()
        cls._start_timer()

        for index, record in enumerate(cls.old_class.objects.using(V1).values()):
            cls.map_record(record, save)
            cls._print_status(record, index)

        cls._done = True
        cls._print_summary()

    @classmethod
    def map_record(cls, record, save=False):
        new = cls.new_class()
        for attribute, value in record.items():
            cls.set_attribute_processed(new, cls._new_fieldname(attribute), value)
        if (save): new.save(using=V2)

    @classmethod
    def set_attribute_processed(cls, object, attribute, value):
        if type(attribute) is tuple and callable(attribute[1]):
            setattr(object, attribute[0], attribute[1](value))
        else:
            setattr(object, attribute, value)

    @classmethod
    def _new_fieldname(cls, attribute):
        if attribute in cls._get_fieldnames().keys():
            return cls._get_fieldnames()[attribute]
        if attribute[:-3] in cls._get_fieldnames().keys():
            return cls._get_fieldnames()[attribute[:-3]] + '_id'
        raise RuntimeError('Attribute not found: ' + attribute)

    @classmethod
    def _get_fieldnames(cls):
        fields = { field_to_str(field): field_to_str(field) for field in cls.old_class._meta.fields }
        fields.update(cls.attributes)
        return fields

    @classmethod
    def _check_dependencies(cls):
        for dependency in cls.depends:
            if not dependency._done: raise RuntimeError("dependency " + str(dependency) + " not done")
    _done = False

    @classmethod
    def _start_timer(cls):
        from time import time
        cls.start_time = time()

    @classmethod
    def _print_status(cls, record, index):
        if not cls._count:
            cls._count = cls.old_class.objects.using(V1).count()
        if index % 10 == 0:
            print(
                "%-30s: %8d (%d/%d)" % (
                    cls.old_class.__name__, int(record['id']), (index + 1), cls._count
                ),
                end="\r"
            )
    _count = 0

    @classmethod
    def _print_summary(cls):
        from time import time
        from datetime import timedelta
        print(
            "%-30s: %8d objects, %s" % (
                cls.old_class.__name__, cls.old_class.objects.using(V1).count(), str(timedelta(seconds=time()-cls.start_time))
            )
        )

def field_to_str(field):
        return str(field).split('.')[-1]
