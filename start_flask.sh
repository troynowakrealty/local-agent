#!/bin/sh
python app.py > flask.log 2>&1 &
echo $! > flask.pid
