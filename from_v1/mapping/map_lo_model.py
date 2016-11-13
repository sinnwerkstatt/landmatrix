from .map_model import MapModel



class MapLOModel(MapModel):

    DB = 'lo'

    @classmethod
    def get_existing_record(cls, record):
        return None

    @classmethod
    def map_record(cls, record, save=False, verbose=False):
        '''
        Overridden to try to make the import safe for multiple runs.
        If there is an existing record, map it to that one.
        '''
        already_imported = cls.get_existing_record(record)

        if already_imported:
            new = already_imported
        else:
            new = cls.new_class()

        for attribute, value in record.items():
            # Don't overwrite ID
            if attribute == 'id':
                continue

            new_fieldname = cls._new_fieldname(attribute)
            cls.set_attribute_processed(new, new_fieldname, value)
            if verbose:
                if isinstance(new_fieldname, tuple):
                    new_fieldname = new_fieldname[0]
                print("%s: '%s' -> %s: '%s'" % (attribute, value, new_fieldname, getattr(new, new_fieldname)))

        cls.save_record(new, record, save)

    @classmethod
    def save_record(cls, new, old, save):
        '''
        Just change the method signature here, but if not implemented call
        super with the old one.
        '''
        return super().save_record(new, save)
