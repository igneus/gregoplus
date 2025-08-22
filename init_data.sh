#!/bin/bash

# Initializes and populates the database.

# Download the GregoBase db dump
mkdir -p db_dump
DUMP_PATH=db_dump/gregobase_online.sql

# latest commit known to work with our codebase:
DUMP_REF=2ebcda3f523f9b19933d59fa32bb4215cd8e7675
# to take the latest version:
# DUMP_REF=refs/heads/master

DUMP_URL=https://github.com/gregorio-project/GregoBase/raw/$DUMP_REF/gregobase_online.sql

# (if executed repeatedly, don't download the large db dump over and over)
if [[ ! -e $DUMP_PATH ]] ; then
  wget -O $DUMP_PATH $DUMP_URL
fi

# Load the dump in the database
if [[ -e .env ]] ; then
  source .env
fi
mariadb --host=$DB_HOST --port=3306 --user=$DB_USER --password=$DB_PASSWORD --skip_ssl $DB_NAME < $DUMP_PATH

# Run migrations
python manage.py migrate --fake-initial
