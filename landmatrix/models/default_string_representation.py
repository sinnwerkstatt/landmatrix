

class DefaultStringRepresentation:

    """ Needs to be the first class inherited from when using it for multiple inheritance,
        if the other classes define a ___str___ method too the implementation of the class
        first in the list of base classes is used.
    """

    indent_depth = 0

    def __str__(self):
        import pprint

        DefaultStringRepresentation.indent_depth += 1

        items = {
            key: self._iteritem_to_object_pair(key, value)
            for (key, value) in vars(self).items()
            if not key.startswith('_')
        }

        ret = pprint.pformat(dict(items), indent=4*DefaultStringRepresentation.indent_depth)

        DefaultStringRepresentation.indent_depth -= 1

        if DefaultStringRepresentation.indent_depth == 0:
            ret = "\n" + ret

        return ret

    def _iteritem_to_object_pair(self, key, value):
        if not self.is_database_relation(key): return value
        if value is None: return None

        object_class = str_to_class(fk_to_class_name(key))
        try:
            return object_class.objects.get(id=int(value))
        except Exception:
            return str(object_class)+'.get('+str(id)+') does not exist'

    def is_database_relation(self, key):
        return key.startswith('fk_')


def fk_to_class_name(str):
        return to_camel_case(str[3:-3])

def str_to_class(str):
        import importlib
        module = importlib.import_module('landmatrix.models')
        try:
            instance = getattr(module, str)()
        except AttributeError:
            return None
        return type(instance)

def to_camel_case(snake_str):
        return "".join(x.title() for x in (snake_str.split('_')))
