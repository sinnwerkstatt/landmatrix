from sys import getsizeof, stderr
from itertools import chain
from collections import deque
from timeit import default_timer

from django.core.management import BaseCommand

from apps.landmatrix.models.deal import Deal

try:
    from reprlib import repr
except ImportError:
    pass


# https://docs.python.org/3.10/library/sys.html#sys.getsizeof
def total_size(obj, handlers=None, verbose=False):
    """Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    if handlers is None:
        handlers = {}
    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: lambda d: chain.from_iterable(d.items()),
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen
    default_size = getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:  # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(obj)


class Command(BaseCommand):
    def handle(self, *args, **options):

        start = default_timer()
        deals = [
            obj for obj in Deal.objects.all().distinct().prefetch_related().values()
        ]
        end = default_timer()

        print(f"query duration {end-start:.3f}s")
        print()

        sizes = sorted(
            [
                {
                    "id": d["id"],
                    "total": total_size(d),
                    "locations": total_size(d["locations"]),
                    "geojson": total_size(d["geojson"]),
                }
                for d in deals
            ],
            key=lambda d: d["total"],
            reverse=True,
        )

        print(f"{'id':<10s}", end="")
        print(f"{'total(MB)':<15s}", end="")
        print(f"{'locations(MB)':<15s}", end="")
        print(f"{'geojson(MB)':<15s}", end="")
        print()

        for d in sizes[:10]:
            print(f"{d['id']:<10d}", end="")
            print(f"{d['total']/1000/1000:<15.3f}", end="")
            print(f"{d['locations']/1000/1000:<15.3f}", end="")
            print(f"{d['geojson']/1000/1000:<15.3f}", end="")
            print()
