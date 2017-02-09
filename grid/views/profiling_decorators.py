from time import time

from django.db import connection
from django.db.backends.base.base import BaseDatabaseWrapper

from functools import wraps



PROFILING_DECORATORS_STFU = True


def print_execution_time_and_num_queries(func):
    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        return print_num_queries(print_execution_time(func))(self, *args, **kwargs)
    return func_wrapper


def method_name(self, func):
    return type(self).__name__ + '.' + func.__name__


def args_to_str(args):
    return str(tuple(str(arg)[:40] for arg in args))


def print_execution_time(func):

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        if PROFILING_DECORATORS_STFU:
            return func(self, *args, **kwargs)
        start = time()
        print_execution_time.call_depth += 1
        result = func(self, *args, **kwargs)
        print_execution_time.call_depth -= 1
        time_used = time() - start
        if time_used > print_execution_time.MIN_TIME_TO_PRINT:
            print('    ' * print_execution_time.call_depth+method_name(self, func)+args_to_str(args), time_used, 's')
        return result

    return func_wrapper

print_execution_time.call_depth = 0
print_execution_time.MIN_TIME_TO_PRINT = 0.01


def print_func_execution_time(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if PROFILING_DECORATORS_STFU:
            return func(*args, **kwargs)
        start = time()
        print_execution_time.call_depth += 1
        result = func(*args, **kwargs)
        print_execution_time.call_depth -= 1
        time_used = time() - start
        if time_used > print_execution_time.MIN_TIME_TO_PRINT:
            print('    ' * print_execution_time.call_depth + func.__name__ + args_to_str(args), time_used, 's')
        return result

    return func_wrapper


def print_num_queries(func):

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        if PROFILING_DECORATORS_STFU:
            return func(self, *args, **kwargs)
        old_db_buffer_length = BaseDatabaseWrapper.queries_limit
        BaseDatabaseWrapper.queries_limit = 100000
        num_queries_old = len(connection.queries)
        print_num_queries.call_depth += 1
        result = func(self, *args, **kwargs)
        print_num_queries.call_depth -= 1
        queries_used = len(connection.queries) - num_queries_old
        if queries_used:
            print(
                '    '*print_num_queries.call_depth+method_name(self, func),
                queries_used, 'queries'
            )
        BaseDatabaseWrapper.queries_limit = old_db_buffer_length
        return result

    return func_wrapper

print_num_queries.call_depth = 0


def print_func_num_queries(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if PROFILING_DECORATORS_STFU:
            return func(*args, **kwargs)
        old_db_buffer_length = BaseDatabaseWrapper.queries_limit
        BaseDatabaseWrapper.queries_limit = 100000
        num_queries_old = len(connection.queries)
        print_num_queries.call_depth += 1
        result = func(*args, **kwargs)
        print_num_queries.call_depth -= 1
        queries_used = len(connection.queries) - num_queries_old
        if queries_used:
            print(
                '    '*print_num_queries.call_depth+func.__name__+args_to_str(args),
                queries_used, 'queries'
            )
        BaseDatabaseWrapper.queries_limit = old_db_buffer_length
        return result

    return func_wrapper


def print_last_query(func):

    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        if PROFILING_DECORATORS_STFU:
            return func(self, *args, **kwargs)
        print_num_queries.call_depth += 1
        result = func(self, *args, **kwargs)
        print_num_queries.call_depth -= 1
        last_query = connection.queries[-1]
        if last_query and last_query.get('sql'):
            print('    '*print_num_queries.call_depth+method_name(self, func)+args_to_str(args)+':')
            print(last_query.get('sql'))
            print()
        return result

    return func_wrapper

print_num_queries.call_depth = 0

def memoize(obj):
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
