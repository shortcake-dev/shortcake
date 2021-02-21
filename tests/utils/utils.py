import collections


def call_counter(func):
    """Keep track of number of times a function has been called and pass
    counter_index to it.

    If counter_index is supplied to the wrapped function, the count will not be
    used nor incremented, and the passed value will be used instead
    """

    # Keep track of number of times a function is called
    count_map = collections.Counter()

    def _func(*args, **kwargs):
        # If counter_index is supplied, use it; otherwise use next in sequence
        # for the func
        counter_index = kwargs.pop("counter_index", None)
        count = count_map[func] if counter_index is None else counter_index

        kwargs["counter_index"] = count
        ret = func(*args, **kwargs)

        # Only increment count if one was not manually specified
        if counter_index is None:
            count_map[func] += 1

        return ret

    return _func
