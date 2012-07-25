#!/bin/bash
#-------------------------------------------------------------------------------
#
# Setup virtualenv and install dependency requirements.
#
#-------------------------------------------------------------------------------

set -x 

virtualenv --no-site-packages venv
source ./venv/bin/activate
time pip install -r requirements.txt
