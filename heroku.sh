#!/bin/bash
#
# Create Pijyn Heroku app
#
heroku create pijyn &&
heroku addons:add sendgrid:starter &&
time git push heroku master
heroku run python manage.py syncdb
#heroku run python manage.py migrate
