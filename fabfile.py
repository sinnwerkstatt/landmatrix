from datetime import datetime

from fabric.api import cd, run, env, local, hide, settings
from fabric.contrib import django
from fabric.operations import get
from fabvenv import virtualenv


def staging():
    env.name = 'staging'
    env.hosts = ['lmlo@lmlo.sinnwerkstatt.com']
    env.path = '/srv/lmlo.sinnwerkstatt.com/lmlo/'
    env.virtualenv_path = '/srv/lmlo.sinnwerkstatt.com/lmloenv'
    env.backup_path = '/srv/lmlo.sinnwerkstatt.com/backups'
    env.push_branch = 'master'
    env.push_remote = 'origin'
    env.reload_cmd = 'supervisorctl restart lmlo'
    env.db_name = 'lmlo'
    env.db_username = 'lmlo'
    env.after_deploy_url = 'http://lmlo.sinnwerkstatt.com'
    
def production():
    pass

def compile_less():
    pass

def reload_webserver():
    run("%(reload_cmd)s" % env)

def migrate():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py syncdb" % env)
        run("%(path)s/manage.py migrate" % env)

def ping():
    run("echo %(after_deploy_url)s returned:  \>\>\>  $(curl --write-out %%{http_code} --silent --output /dev/null %(after_deploy_url)s)" % env)
    
def deploy():
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)
        compile_less()
        with virtualenv(env.virtualenv_path):
            run("pip install -Ur requirements.txt")
            run("./manage.py collectstatic --noinput")

    migrate()
    reload_webserver()
    ping()
    
def init_fixtures():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py loaddata init.json" % env)
        
def update():
    ''' Only deploy and reload modules from git, do no installing or migrating'''
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)
        compile_less()
        with virtualenv(env.virtualenv_path):
            run("./manage.py collectstatic --noinput")
        
    reload_webserver()
    
def backup():
    with cd(env.backup_path):
        run("pg_dump -U %(db_username)s %(db_name)s > %(db_name)s_backup_$(date +%%F-%%T).sql" % env)
        run("ls -lt")

def rebuild_index():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py rebuild_index -v 2" % env)

def update_index():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py update_index -v 2" % env)
