#!/bin/bash
python3 app.py > flask.log 2>&1 &
echo $! > flask.pid
