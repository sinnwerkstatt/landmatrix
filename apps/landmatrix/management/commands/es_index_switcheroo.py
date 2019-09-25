import os

from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Update deal index for elasticsearch in A/B manner"

    def handle(self, *args, **options):
        new_index = "a" if settings.ELASTIC_INDEX_AB == "b" else "b"
        settings.ELASTICSEARCH_INDEX_NAME = (
            f"{settings.ELASTICSEARCH_INDEX_BASENAME}_{new_index}"
        )

        print(f"running index update on {settings.ELASTICSEARCH_INDEX_NAME}")
        call_command("search_index", "--rebuild")

        # switch the index after the new one has been built
        open(".es_index_ab_switch", "w").write(new_index)

        # try and reload gunicorn
        from pathlib import Path

        gunicornpid = int(open(f"{Path.home()}/run/gunicorn.pid", "r").read())
        os.kill(gunicornpid, 1)  # signal.SIGHUP == 1
