#!/bin/bash

source venv/bin/activate
export FLASK_APP=jams01.py
export OAUTHLIB_INSECURE_TRANSPORT=1
flask run
