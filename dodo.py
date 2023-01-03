#!/usr/bin/env python3
from glob import glob

import environ
from doit import get_var

env = environ.Env()
env.read_env(".env")

DOIT_CONFIG = {"default_tasks": ["update"], "verbosity": 2}


def pg_run(cmd: str, database="") -> str:
    return f'sudo -Hiu postgres psql {database} -c "{cmd}"'


def task_update():
    return {"task_dep": ["collectstatic", "compilemessages", "migrate"], "actions": []}


def task_full_update():
    return {"task_dep": ["git_pull", "poetry_install", "update"], "actions": []}


def task_initial_setup():
    fixtures = " ".join(["countries_and_regions", "users_and_groups"])
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
def task_frontend_build():
    actions = ["cd frontend; npm ci", "cd newfront; npm ci"]
    if get_var("production", False):
        actions += ["cd frontend; npm run build"]
        actions += ["cd newfront; npm run build"]
    return {
        "task_dep": ["compilemessages"],
        "actions": actions,
    }


def task_collectstatic():
    return {
        "task_dep": ["frontend_build"],
        "actions": ["./manage.py collectstatic --noinput"],
    }


def task_compilemessages():
    for pofile in glob("config/locale/**/LC_MESSAGES/*.po", recursive=True):
        mofile = pofile[:-2] + "mo"
        json_target = f"frontend/src/i18n_messages.{pofile[14:16]}.json"
        new_target = f"newfront/src/lib/i18n/lang_{pofile[14:16]}.json"
        englishhack = "python plumbing/i18n_helpers.py" if "es" in pofile else ""
        englishhack_newfront = (
            f"cp frontend/src/i18n_messages.en.json newfront/src/lib/i18n/lang_en.json"
            if "es" in pofile
            else ""
        )

        yield {
            "name": pofile,
            "file_dep": [pofile],
            "targets": [mofile, json_target, new_target],
            "actions": [
                f"msgfmt -o {mofile} {pofile}",
                f"python plumbing/pojson.py {pofile} > {json_target}",
                f"cp {json_target} {new_target}",
                englishhack,
                englishhack_newfront,
                f"""sed -i -e '/.*: "",$/d' {json_target}""",
            ],
            "clean": True,
        }


def task_migrate():
    return {"actions": ["./manage.py migrate --noinput"]}


def task_git_pull():
    branch = get_var("branch", "main")
    return {"actions": [f"git checkout {branch}", "git pull"]}


def task_poetry_install():
    dev = "--no-dev" if not get_var("dev", False) else ""
    return {"actions": [f"poetry install {dev}"]}
