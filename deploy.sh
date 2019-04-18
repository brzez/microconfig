PORT=/dev/ttyUSB0

ampy -p $PORT put main.py
ampy -p $PORT put info.py
ampy -p $PORT put microconfig.py
ampy -p $PORT put heartbeat.py
ampy -p $PORT mkdir webserver
ampy -p $PORT put webserver/__init__.py ./webserver/__init__.py
ampy -p $PORT put webserver/form.py ./webserver/form.py
ampy -p $PORT put webserver/unquote.py ./webserver/unquote.py
ampy -p $PORT put form.html
ampy -p $PORT put page.html
ampy -p $PORT put misc.py

sleep 1
echo "resetting board..."
ampy -p $PORT reset
