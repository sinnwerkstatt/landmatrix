#!/usr/bin/env python3
from glob import glob

import environ

env = environ.Env()
env.read_env(".env")

DOIT_CONFIG = {"default_tasks": ["update"], "verbosity": 2}


def task_update():
    return {"task_dep": ["collectstatic", "compilemessages", "migrate"], "actions": []}


def task_initial_setup():
    return {
        "task_dep": ["update"],
        "actions": [
            "./manage.py loaddata status languages crops animals minerals countries_and_regions users_and_groups filters",
            "./manage.py initial_setup",
        ],
    }


def task_reset_db():
    db = env.db()
    actions = []

    if "postgis" in db["ENGINE"] or "postgresql" in db["ENGINE"]:
        actions = [
            f"sudo -u postgres psql -c 'drop database {db['NAME']}' || true",
            f"sudo -u postgres psql -c 'create database {db['NAME']} with owner {db['USER']}'",
        ]
        if "postgis" in db["ENGINE"]:
            actions += [
                f"sudo -u postgres psql {db['NAME']} -c 'create extension postgis'"
            ]

    elif db["ENGINE"] == "django.db.backends.sqlite3":
        actions = [f"rm -f {db['NAME']}"]

    return {"actions": actions}


#############################
def task_yarn_install():
    return {"targets": ["node_modules/"], "actions": ["/usr/bin/yarn install"]}


def task_convert_scss():
    for scss in glob("apps/landmatrix/static/css/[a-z]*.scss", recursive=True):
        css = scss[:-4] + "css"
        yield {
            "name": scss,
            "file_dep": [scss],
            "targets": [css],
            "actions": [f"pysassc {scss} > {css}"],
            "clean": True,
        }


def task_collectstatic():
    return {
        "task_dep": ["yarn_install", "convert_scss"],
        "actions": ["./manage.py collectstatic --noinput"],
    }


def task_compilemessages():
    for pofile in glob("**/LC_MESSAGES/*.po", recursive=True):
        mofile = pofile[:-2] + "mo"
        yield {
            "name": pofile,
            "file_dep": [pofile],
            "targets": [mofile],
            "actions": [f"msgfmt -o {mofile} {pofile}"],
            "clean": True,
        }


def task_migrate():
    return {"actions": ["./manage.py migrate --noinput"]}
