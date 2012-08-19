#!/bin/bash
#
# Create Pijyn Heroku app
#
heroku create pijyn &&
heroku addons:add sendgrid:starter &&
time git push heroku master
heroku run python manage.py syncdb
#heroku run python manage.py migrate
echo Be sure to run "heroku config:set GOOGLE_OAUTH2_CLIENT_ID=your_client_id"
echo and "heroku config:set GOOGLE_OAUTH2_CLIENT_SECRET=your_client_secret"
