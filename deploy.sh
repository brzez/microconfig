PORT=/dev/ttyUSB0

ampy -p $PORT put main.py
ampy -p $PORT put microconfig.py
ampy -p $PORT mkdir mqtt
ampy -p $PORT put mqtt/__init__.py ./mqtt/__init__.py
ampy -p $PORT put mqtt/umqttsimple.py ./mqtt/umqttsimple.py
exit 0
ampy -p $PORT put info.py
ampy -p $PORT put heartbeat.py
ampy -p $PORT mkdir webserver
ampy -p $PORT put webserver/__init__.py ./webserver/__init__.py
ampy -p $PORT put webserver/form.py ./webserver/form.py
ampy -p $PORT put webserver/unquote.py ./webserver/unquote.py
ampy -p $PORT mkdir views
ampy -p $PORT put views/microconfig.html ./views/microconfig.html
ampy -p $PORT put misc.py

sleep 1
echo "resetting board..."
ampy -p $PORT reset
