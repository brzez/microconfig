PORT=/dev/ttyUSB0

ampy -p $PORT put main.py
ampy -p $PORT put form.py
ampy -p $PORT put webserver.py
ampy -p $PORT put form.html
ampy -p $PORT put page.html
ampy -p $PORT put misc.py
ampy -p $PORT put unquote.py

sleep 1
echo "resetting board..."
ampy -p $PORT reset
