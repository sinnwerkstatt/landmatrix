from timeit import default_timer


class Timer:
    """Custom Timer class."""

    def __init__(self, name: str):
        self._name = name
        self._start_time = None

    def __enter__(self):
        """Start a new timer as a context manager"""
        self._start_time = default_timer()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        duration = default_timer() - self._start_time
        self._start_time = None

        print(f"Runtime {self._name}: {duration:0.3f}s")
