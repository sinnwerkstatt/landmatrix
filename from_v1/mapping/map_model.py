from migrate import V1, V2

from django.db import transaction



class MapModel:
    """
        Map a model from Landmatrix V1 to Landmatrix V2.
        Usage:
        - Subclass MapModel
        - set the class variables old_class and new_class to the models in V1 and V2
        - optionally:
          - set the class variable depends to a list of mappings that need to be run before this
          - set the class variable attributes to a dict of mappings of old attribute names to new attribute names
          - optionally, the second parameter of the mapping can be a pair of (new_attribute_name, processing_function)
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

    attributes = { }
    depends = []
    DEBUG = False
    DB = V1

    @classmethod
    def map(cls, id, save=False):
        record = cls.old_class.objects.using(cls.DB).filter(id=id).values()[0]
        cls.map_record(record, save)

    @classmethod
    @transaction.atomic(using=V2)
    def map_all(cls, save=False, verbose=False):

        cls._check_dependencies()
        cls._start_timer()

        for index, record in enumerate(cls.all_records()):
            cls.map_record(record, save, verbose)
            cls._print_status(record, index)

        cls._done = True
        cls._print_summary()

    @classmethod
    def all_records(cls):
        return cls.old_class.objects.using(cls.DB).values()

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        new = cls.new_class()
        for attribute, value in record.items():
            new_fieldname = cls._new_fieldname(attribute)
            cls.set_attribute_processed(new, new_fieldname, value)
            if verbose:
                if isinstance(new_fieldname, tuple):
                    new_fieldname = new_fieldname[0]
                print("%s: '%s' -> %s: '%s'" % (attribute, value, new_fieldname, getattr(new, new_fieldname)))

        cls.save_record(new, save)

    @classmethod
    def save_record(cls, new, save):
        """Extracted because subclasses might need to pass extra parameters to Model.save()"""
        if save:
            new.save(using=V2)

    @classmethod
    def set_attribute_processed(cls, object, attribute, value):
        """
        attribute can be any of the following:
        - None. Then the attribute/value combination is ignored on the processed object.
        - The name of the attribute as a string. Then the processed object's attribute with the name attribute is set to
          value.
        - A 2-tuple, first the name of the attribute as string and second a function to process value with. The
          processed object's attribute with the name attribute[0] is set to attribute[1](value).
        - An n-tuple, each element being either the name of an attribute or a pair of attribute names/processing functions.
          Each of the tuple's elements is treated for  the same value.
        """

        if type(attribute) is tuple and len(attribute) == 1:
            attribute = attribute[0]

        if attribute is None:
            return

        if type(attribute) is tuple and callable(attribute[1]):
            if cls.DEBUG:
                print(
                    'set attribute %s to %s, i.e. %s after processing with %s' % (attribute[0], attribute[1](value), value, attribute[1].__name__)
                )
            setattr(object, attribute[0], attribute[1](value))
        elif type(attribute) is tuple:
            if cls.DEBUG:
                print('set attributes %s to value %s' % (str(attribute), value))
            cls.set_attribute_processed(object, attribute[0], value)
            cls.set_attribute_processed(object, attribute[1:], value)
        else:
            if cls.DEBUG:
                print('set attribute %s to value %s' % (attribute, value))
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
            cls._count = cls.old_class.objects.using(cls.DB).count()
        if index % 10 == 0:
            print(
                "%-50s: %8d (%d/%d)" % (
                    mapping_name(cls), record.get('id') if record.get('id') else 0, (index + 1), cls._count
                ),
                end="\r"
            )
    _count = 0

    @classmethod
    def _print_summary(cls):
        from time import time
        from datetime import timedelta
        print(
            "%-50s: %8d objects, %s" % (
                mapping_name(cls), cls._count, str(timedelta(seconds=time()-cls.start_time))
            )
        )


def field_to_str(field):
        return str(field).split('.')[-1]


def mapping_name(cls):
    return '%s (%s)' % (cls.__name__, cls.old_class.__name__)