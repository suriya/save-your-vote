#!/usr/bin/env bash

SCRIPT_DIR=`dirname $0`

MEDIA_DIR=$SCRIPT_DIR/../../media
rm -rfv $MEDIA_DIR
mkdir -p $MEDIA_DIR
rm -fv $SCRIPT_DIR/../../sqlite3.db
$SCRIPT_DIR/../manage.py syncdb --noinput
python $SCRIPT_DIR/add-states.py
python $SCRIPT_DIR/add-ka-districts.py
