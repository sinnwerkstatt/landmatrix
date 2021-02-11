#!/usr/bin/env python3
from glob import glob

import environ
from doit import get_var

env = environ.Env()
env.read_env(".env")

DOIT_CONFIG = {"default_tasks": ["update"], "verbosity": 2}


def pg_run(cmd: str, database="") -> str:
    return f"sudo -u postgres psql {database} -c '{cmd}'"


def task_update():
    return {"task_dep": ["collectstatic", "compilemessages", "migrate"], "actions": []}


def task_full_update():
    return {"task_dep": ["git_pull", "poetry_install", "update"], "actions": []}


def task_initial_setup():
    fixtures = " ".join(
        [
            "status",
            "languages",
            "crops",
            "animals",
            "minerals",
            "countries_and_regions",
            "users_and_groups",
            "filters",
        ]
    )
    return {
        "task_dep": ["update"],
        "actions": [
            f"./manage.py loaddata {fixtures}",
            "./manage.py initial_setup",
        ],
    }


def task_reset_db():
    db = env.db()
    actions = []

    if "postgis" in db["ENGINE"] or "postgresql" in db["ENGINE"]:
        actions = [
            pg_run(f"DROP DATABASE IF EXISTS {db['NAME']}"),
            pg_run(f"CREATE DATABASE {db['NAME']} WITH OWNER {db['USER']}"),
        ]
        if "postgis" in db["ENGINE"]:
            actions += [
                pg_run(f"CREATE EXTENSION IF NOT EXISTS postgis"),
            ]

    elif db["ENGINE"] == "django.db.backends.sqlite3":
        actions = [f"rm -f {db['NAME']}"]

    return {"actions": actions}


#############################
def task_npm_install():
    actions = ["npm install"]
    if get_var("production", False):
        actions += ["npm run build_frontend"]
    return {
        "task_dep": ["compilemessages"],
        "targets": ["node_modules/"],
        "actions": actions,
    }


def task_convert_scss():
    for scss in glob("apps/landmatrix/static/css/[a-z]*.scss", recursive=True):
        css = scss[:-4] + "css"
        yield {
            "name": f"pysassc {scss} {css}",
            "file_dep": [scss],
            "targets": [css],
            "actions": [f"pysassc {scss} {css}"],
            "clean": True,
        }


def task_collectstatic():
    return {
        "task_dep": ["npm_install", "convert_scss"],
        "actions": ["./manage.py collectstatic --noinput"],
    }


def task_compilemessages():
    for pofile in glob("config/locale/**/LC_MESSAGES/*.po", recursive=True):
        mofile = pofile[:-2] + "mo"
        json_target = f"frontend/src/i18n_messages.{pofile[14:16]}.json"
        yield {
            "name": pofile,
            "file_dep": [pofile],
            "targets": [mofile, json_target],
            "actions": [
                f"msgfmt -o {mofile} {pofile}",
                f"npx po2json -p -f mf {pofile} {json_target}",
                f"""sed -i -e '/.*: "",$/d' {json_target}""",
            ],
            "clean": True,
        }


def task_migrate():
    return {"actions": ["./manage.py migrate --noinput"]}


def task_git_pull():
    branch = get_var("branch", "master")
    return {"actions": [f"git checkout {branch}", "git pull"]}


def task_poetry_install():
    dev = "--no-dev" if not get_var("dev", False) else ""
    prod = "-E production" if get_var("production", False) else ""
    return {"actions": [f"poetry install {dev} {prod}"]}


def task_get_db_from_production():
    return {
        "actions": [
            """ssh landmatrix@landmatrix.org "pg_dump landmatrix | bzip2" > landmatrix.sql.bz2"""
        ]
    }


def task_reset_db_with_dump():
    replace_db = """bzcat landmatrix.sql.bz2 | psql landmatrix"""
    reset_site_to_localhost = pg_run(
        "UPDATE wagtailcore_site SET port=8000, hostname='localhost'",
        database="landmatrix",
    )
    return {
        "task_dep": ["reset_db"],
        "actions": [replace_db, reset_site_to_localhost],
    }
