#! /bin/sh

# python manage.py dumpdata --indent=2 auth.group auth.user specialname.product > fixtures.json
# python manage.py loaddata fixtures.json


cd /home/ec2-user/specialname
sudo chown  -R root ./static/
# sudo chown  -R root ./db.sqlite3
# sed -i  "s/\"sandbox/\"live/g" specialname/views/view_specialname.py
python manage.py collectstatic --noinput
gunicorn --workers=2  mysite.wsgi:application &

