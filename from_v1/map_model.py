__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from migrate import V1, V2

from django.db import models

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

        cls._check_dependencies()

        new = cls.new_class()
        cls._copy_attributes(cls.old_class.objects.using(V1).get(id=id), new)

        if save:
            new.save(using=V2)

    @classmethod
    def map_all(cls, save=False):
        cls._start_timer()

        for index, id in enumerate(cls.old_class.objects.using(V1).values('id')):
            cls.map(id['id'], save=save)
            cls._print_status(id, index)

        cls._done = True
        cls._print_summary()


    @classmethod
    def _start_timer(cls):
        from time import time
        cls.start_time = time()

    @classmethod
    def _print_status(cls, id, index):
        print(
            "%-16s: %7d (%d/%d)" % (
                cls.old_class.__name__, int(id['id']), (index + 1), cls.old_class.objects.using(V1).count()
            ),
            end="\r"
        )

    @classmethod
    def _print_summary(cls):
        from time import time
        from datetime import timedelta
        print(
            "%-16s: %8d objects, %s" % (
                cls.old_class.__name__, cls.old_class.objects.using(V1).count(), str(timedelta(seconds=time()-cls.start_time))
            )
        )

    @classmethod
    def _check_dependencies(cls):
        for dependency in cls.depends:
            if not dependency._done: raise RuntimeError("dependency " + str(dependency) + " not done")
    _done = False

    @classmethod
    def _copy_attributes(cls, old, new):
        for (old_attribute, new_attribute) in cls._get_fieldnames().items():
            cls._process_and_copy_attribute(old, old_attribute, new, new_attribute)

    @classmethod
    def _process_and_copy_attribute(cls, old, old_attribute, new, new_attribute):
        if type(new_attribute) is tuple and callable(new_attribute[1]):
            setattr(new, new_attribute[0], new_attribute[1](getattr(old, old_attribute)))
        else:
            setattr(new, new_attribute, cls._get_attribute(old, old_attribute, new_attribute))

    @classmethod
    def _get_attribute(cls, old, old_attribute, new_attribute):
        return cls._get_related(new_attribute, old, old_attribute) if cls._is_relation(new_attribute) else getattr(old, old_attribute)

    @classmethod
    def _get_fieldnames(cls):
        fields = { cls._field_to_str(field): cls._field_to_str(field) for field in cls.old_class._meta.fields }
        fields.update(cls.attributes)
        return fields

    @classmethod
    def _field_to_str(cls, field):
        return str(field).split('.')[-1]

    @classmethod
    def _is_relation(cls, fieldname):
        return type(cls._get_field(fieldname)) is models.ForeignKey

    @classmethod
    def _get_field(cls, fieldname):
        return cls.new_class._meta.get_field(fieldname)

    @classmethod
    def _get_related(cls, new_attribute, old, old_attribute):
        if getattr(old, old_attribute) is None: return None
        related_class = cls._get_field(new_attribute).rel.to
        return related_class.objects.using(V2).get(id=getattr(old, old_attribute).id)
