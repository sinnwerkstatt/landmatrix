import re
from functools import wraps


def db_require_confirmation(fn):

    @wraps(fn)
    def wrapped(*args, **kwargs):
        confirm = input(
            "***** ATTENTION ***** \n"
            "This command potentially manipulates DB. \n"
            "Make sure DB connection is configured correctly in .env. \n"
            "Confirm to continue (y/N): "
        )

        if not confirm or not re.match("^y(es)?$", confirm, re.I):
            print("Aborting")
            return

        fn(*args, **kwargs)

    return wrapped
