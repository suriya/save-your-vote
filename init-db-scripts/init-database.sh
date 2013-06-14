#!/usr/bin/env bash

SCRIPT_DIR=$(readlink -f `dirname $0`)

export DJANGO_SETTINGS_MODULE=saveyourvote.settings
export PYTHONPATH=${SCRIPT_DIR}/../:$PYTHONPATH

# MEDIA_DIR=$SCRIPT_DIR/../../media
# rm -rfv $MEDIA_DIR
# mkdir -p $MEDIA_DIR
rm -fv $SCRIPT_DIR/../sqlite3.db
$SCRIPT_DIR/../manage.py syncdb --noinput
python $SCRIPT_DIR/add-states.py
python $SCRIPT_DIR/add-ka-districts.py
python $SCRIPT_DIR/add-up-districts.py
python $SCRIPT_DIR/add-districts.py
python $SCRIPT_DIR/add-flatpages.py
