from fabric.api import local, run, warn_only
from fabric.context_managers import cd, shell_env, settings
from fabric import colors
from fabric.utils import abort, puts

def host_type():
    """fab host_type -H 54.69.158.70 -u root
    """
    run('uname -s')


def ver():
    """fab ver
    """
    local('fab --version')
    local('python --version')
    local('python manage.py version')


def post_deploy():
    """fab post_deploy
    """

    local('cd ~/specialname')
    # local('rm sqlite3_db')
    local('git pull')
    # local('chown www-data .')
    # local('chown www-data ./sqlite3_db')
    # local('chmod u+w+x,g+w+x ./sqlite3_db')
    local('python manage.py migrate')
    local('python manage.py collectstatic --noinput')
    #local('/etc/init.d/apache2 restart')
    local('pkill gunicorn')
    local('gunicorn --workers=2 mysite.wsgi:application &')


def loaddata():
    # local('python manage.py loaddata peggy/fixtures/peggy.json')
    puts(colors.green("fixtures."))

def deploy():
    """
    fab deploy -H 54.69.158.70 -u root
    """
    with shell_env(SERVER_SOFTWARE='1'):
        with cd('~/speciname/'):
            run('echo $SERVER_SOFTWARE')
            run('git pull')
            # run('chown www-data .')
            # run('chown www-data ./sqlite3_db')
            # run('chmod u+w+x,g+w+x ./sqlite3_db')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
            run('python manage.py loaddata fixtures.json')
            #run('/etc/init.d/apache2 restart')
            restart()


def restart():
    """
    fab restart -H 54.69.158.70 -u root
    """
        with cd('~/speciname/'):
        # run('./s.sh')
        with settings(warn_only=True):
            run('pkill gunicorn')
        run('gunicorn --workers=2 mysite.wsgi:application')
        # run("nohup gunicorn --workers=2 mysite.wsgi:application >& /dev/null < /dev/null &")