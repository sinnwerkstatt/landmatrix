__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from migrate import V1, V2

from django.db import models

class MapModel:

    attributes = { }

    @classmethod
    def map(cls, id, printit=False, save=False):
        old = cls.old_class.objects.using(V1).get(id=id)
        new = cls.new_class()
        cls._copy_attributes(old, new)

        if printit:
            print(old, new)
        if save:
            new.save(using=V2)

    @classmethod
    def map_all(cls):
        for index, id in enumerate(cls.old_class.objects.using(V1).values('id')):
            print(index+1, '/', cls.old_class.objects.using(V1).count(), end="\r")
            cls.map(id['id'])
        print()


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
        related_class = cls._get_field(new_attribute).rel.to
        return related_class.objects.using(V2).get(id=getattr(old, old_attribute).id)
