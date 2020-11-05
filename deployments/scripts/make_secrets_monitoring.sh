#!/bin/bash
ENV="k8s-master"
DIR_BASE="$(dirname $(realpath $0))"
DIR_ENV="$DIR_BASE/$ENV"
NAMESPACE="monitoring"
SECRET_NAME="secrets-$ENV"
HELP="Usage: ./make_secrets_monitoring.sh"

# testing env
TESTING_DB_USER="$(cat production/pss_db_user)"
TESTING_DB_PASSWORD="$(cat production/pss_db_user)"
TESTING_DB_HOST="incrudibles-production.db.pdl.cmu.edu"
TESTING_DB_PORT="30002"
TESTING_DB_NAME="postgresql://$TESTING_DB_USER:$TESTING_DB_PASSWORD@$TESTING_DB_HOST:$TESTING_DB_PORT/?sslmode=disable"
# staging env
STAGING_DB_USER="$(cat staging/pss_db_user)"
STAGING_DB_PASSWORD="$(cat staging/pss_db_user)"
STAGING_DB_HOST="incrudibles-staging.db.pdl.cmu.edu"
STAGING_DB_PORT="31002"
STAGING_DB_NAME="postgresql://$STAGING_DB_USER:$STAGING_DB_PASSWORD@$STAGING_DB_HOST:$STAGING_DB_PORT/?sslmode=disable"
# production env
PRODUCTION_DB_USER="$(cat production/pss_db_user)"
PRODUCTION_DB_PASSWORD="$(cat production/pss_db_user)"
PRODUCTION_DB_HOST="incrudibles-production.db.pdl.cmu.edu"
PRODUCTION_DB_PORT="32002"
PRODUCTION_DB_NAME="postgresql://$PRODUCTION_DB_USER:$PRODUCTION_DB_PASSWORD@$PRODUCTION_DB_HOST:$PRODUCTION_DB_PORT/?sslmode=disable"
# overall postgres db names
DB_NAMES="$TESTING_DB_NAME,$STAGING_DB_NAME,PRODUCTION_DB_NAME"
printf $DB_NAMES > $DIR_ENV/pss_db_data_sources

if [ ! -d $DIR_ENV ]; then
    echo "Error: secrets files for '$ENV' is not found."
    exit 1
fi

kubectl create secret generic $SECRET_NAME -n $NAMESPACE --from-file=$DIR_ENV