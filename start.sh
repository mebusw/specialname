#! /bin/sh

# python manage.py runserver

cd /home/ec2-user/specialname
sudo chown  -R root ./static/
sudo chown  -R root ./db.sqlite3
python manage.py collectstatic --noinput
gunicorn --workers=2  mysite.wsgi:application &

