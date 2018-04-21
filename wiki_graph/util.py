import collections
import itertools
import sys


def rec_sizeof(o, handlers={}, verbose=False):
    """Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    def dict_handler(d):
        return itertools.chain.from_iterable(d.items())

    all_handlers = {tuple: iter,
                    list: iter,
                    collections.deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter}
    # user handlers take precedence
    all_handlers.update(handlers)
    # track which object id's have already been seen
    seen = set()
    # estimate sizeof object without __sizeof__
    default_size = sys.getsizeof(0)

    def sizeof(o):
        # do not double count the same object
        if id(o) in seen:
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=sys.stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)
