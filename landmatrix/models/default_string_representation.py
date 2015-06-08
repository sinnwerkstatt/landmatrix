__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


""" Needs to be the first class inherited from when using it for multiple inheritance,
    if the other classes define a ___str___ method too the implementation of the class
    first in the list of base classes is used.
"""
class DefaultStringRepresentation:

    indent_depth = 0

    def __str__(self):

        DefaultStringRepresentation.indent_depth += 1

        import pprint

        items = {
            key: self._iteritem_to_object_pair(key, value)
            for (key, value) in vars(self).items()
            if not key.startswith('_')
        }
        ret = pprint.pformat(dict(items), indent=4*DefaultStringRepresentation.indent_depth)#. \
#                    replace('{', "{\n"+" "*DefaultStringRepresentation.indent_depth)
        DefaultStringRepresentation.indent_depth -= 1
        return ret

    def _iteritem_to_object_pair(self, key, value):
        if not key.startswith('fk_'): return value
        if value is None: return None
        object_class = str_to_class(fk_to_class_name(key))
        try:
            return object_class.objects.get(id=int(value))
        except Exception:
            return str(object_class)+'.get('+str(id)+') does not exist, last id is '+str(object_class.objects.last().id)


def fk_to_class_name(str):
        return to_camel_case(str[3:-3])

def str_to_class(str):
        import importlib
        module = importlib.import_module('landmatrix.models')
        instance = getattr(module, str)()
        return type(instance)

def to_camel_case(snake_str):
        return "".join(x.title() for x in (snake_str.split('_')))
