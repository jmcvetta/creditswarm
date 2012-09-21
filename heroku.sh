#!/bin/bash
#
# Install Heroku Addons required to run Credit Swarm
#
heroku addons:add sendgrid:starter &&
heroku addons:add cloudamqp:lemur &&
heroku addons:add memcachier:dev
