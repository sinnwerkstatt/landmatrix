__author__ = 'lene'



""" Needs to be the first class inherited from when using it for multiple inheritance,
    if the other classes define a ___str___ method too the implementation of the class
    first in the list of base classes is used.
"""
class DefaultStringRepresentation:
    def __str__(self):
        return str(dict(filter(lambda item: not item[0].startswith('_'), vars(self).items())))