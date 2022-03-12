#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo 'Need the name and password'
    exit 0
fi
NAME="$1"
PASSWORD="$2"
PORT="${3:-80}"

./new_wordpress_from_source.sh $NAME $PASSWORD $PORT plugins

