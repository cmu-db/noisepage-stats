#!/bin/bash

# This script is run on daily basis as a cronjob
# 0 0 * * * /bin/bash /data/scripts/backup_timescale.sh > /dev/null

STR_DATE="$(date '+%Y_%m_%d')"
DIR_TIMESCALEDB="/data/backup/timescaledb"
FILE_BACKUP="$DIR_TIMESCALEDB/timescaledb_dump_$STR_DATE.sql"
CLEAN_CYCLE=5

# timescaledb info
PRODUCTION_DB_USER="$(cat /data/secrets/production/pss_db_user)"
PRODUCTION_DB_PASSWORD="$(cat /data/secrets/production/pss_db_password)"
PRODUCTION_DB_HOST="incrudibles-production.db.pdl.cmu.edu"
PRODUCTION_DB_PORT="32003"
PRODUCTION_DB_NAME="postgresql://$PRODUCTION_DB_USER:$PRODUCTION_DB_PASSWORD@$PRODUCTION_DB_HOST:$PRODUCTION_DB_PORT/pss_database?sslmode=disable"

# install pg_dump if not installed
which pg_dump > /dev/null
if [ $? -ne 0 ]; then
    sudo /usr/bin/apt update -y
    sudo /usr/bin/apt install postgresql-client
fi

# create the timescaledb backup dir if not exists
/bin/mkdir $DIR_TIMESCALEDB

# dump the timescaledb
/usr/bin/pg_dump -d $PRODUCTION_DB_NAME -f $FILE_BACKUP

# delete redundant outdated backups
/usr/bin/find $DIR_TIMESCALEDB/* -mtime +$CLEAN_CYCLE -delete
