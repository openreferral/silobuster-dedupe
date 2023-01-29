#! /bin/bash

cd /var/www/deduper
# python3 deduper.py

# Tail will keep the container open for testing purposes
# If the server wont start, comment out the runserver and uncomment the tail command.
# tail -f /dev/null

python3 manage.py runserver 0.0.0.0:8000