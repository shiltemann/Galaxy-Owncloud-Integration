#!/bin/bash
# owncloud_send.sh "$server/remote.php/webdav/$filename" "$inputfile" "$targetpath"

if [ -z "$OWNCLOUD_SERVER_URL" ]; then
    echo "$OWNCLOUD_SERVER_URL environment variable is not set"
    exit 1
fi
if [ -z "$OWNCLOUD_USERNAME" ]; then
    echo "OWNCLOUD_USERNAME environment variable is not set"
    exit 1
fi
if [ -z "$OWNCLOUD_PASSWORD" ]; then
    echo "OWNCLOUD_PASSWORD environment variable is not set"
    exit 1
fi

# Trim whitespace through xargs
owncloud_url=`echo $OWNCLOUD_SERVER_URL | xargs`
owncloud_username=`echo $OWNCLOUD_USERNAME | xargs`
owncloud_password=`echo $OWNCLOUD_PASSWORD | xargs`
input_datafile=$1
owncloud_targetpath=$2
owncloud_targetfile=$3
owncloud_filename="$owncloud_targetpath$owncloud_targetfile"

# send file to owncloud
curl --silent --show-error --fail --retry 2 -X PUT "$owncloud_url/$owncloud_filename" -u "$owncloud_username:$owncloud_password" --data-binary @"$input_datafile"
