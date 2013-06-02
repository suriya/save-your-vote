
rm -f ../sqlite3.db
./manage.py syncdb --noinput
python ./add-states.py
python ./add-ka-districts.py
