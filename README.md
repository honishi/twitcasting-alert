twitcasting alert
==
monitoring specified user's twitcasting and tweet when live starts.

<!-- ![screenshot](./sample/screenshot.png) -->

setup
--
````
pyenv virtualenv 3.3.3 twitcasting-alert-3.3.3
pyenv local twitcasting-alert-3.3.3
pip install -r requirements.txt
````

start & stop
--
````
./tcalert.sh start
./tcalert.sh stop
````

monitoring example using cron
--
see `tcalert.sh` inside for details of monitoring.
````
* * * * * /path/to/twitcasting-alert/tcalert.sh monitor >> /path/to/twitcasting-alert/log/monitor.log 2>&1 
````

license
--
MIT License.
copyright (c) 2013 honishi, hiroyuki onishi
