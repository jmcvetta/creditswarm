#!/bin/bash
#
# Create Pijyn Heroku app
#
heroku create pijyn &&
heroku addons:add sendgrid:starter &&
heroku addons:add cloudamqp:lemur &&
time git push heroku master &&
heroku run python manage.py syncdb
