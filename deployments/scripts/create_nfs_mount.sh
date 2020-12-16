#!/bin/bash
REMOTE_DIR="basket.pdl.local.cmu.edu:/cmudb-testingteam-backup"
LOCAL_DIR="/data/backup"

# install nfs-common if not installed
which mount > /dev/null
if [ $? -ne 0 ]; then
    sudo apt update -y
    sudo apt install nfs-common
fi

# create the local backup dir if not exists
mkdir -p $LOCAL_DIR

# mount the local backup dir to remote nfs if not mounted
if [ "$(stat -f -L -c %T $LOCAL_DIR)" != "nfs" ]; then 
    mount $REMOTE_DIR $LOCAL_DIR
fi
