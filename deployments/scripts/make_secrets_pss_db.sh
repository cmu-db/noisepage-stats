#!/bin/bash
ENV=$1
DIR_BASE="$(dirname $(realpath $0))"
DIR_ENV="$DIR_BASE/$ENV"
NAMESPACE="performance"
SECRET_NAME="pss-db-secrets-$ENV"
HELP="Usage: ./make_secrets_pss_db.sh ENV"

if [ $# -lt 1 ]; then
    echo $HELP
    exit 1
fi

if [ ! -d $DIR_ENV ]; then
    echo "Error: secrets files for '$ENV' is not found."
    exit 1
fi

kubectl create secret generic $SECRET_NAME -n $NAMESPACE \
    --from-file=$ENV/pss_db_user \
    --from-file=$ENV/pss_db_password