#!/usr/bin/env bash

set -e

basedir=$(cd $(dirname $0);pwd)
program=${basedir}/main.py
logfile=${basedir}/log/tcalert.log
nohupfile=${basedir}/log/nohup.out
pgrep_target="python ${program}"
monitor_threshold=$((1*60))
customenv=${basedir}/tcalert.env

start() {
  if [ 0 -lt $(pgrep -f "${pgrep_target}" | wc -l) ]
  then
    echo "already started."
  else
    nohup ${program} >> ${nohupfile} 2>&1 &
  fi
}

stop() {
  pkill -f "${pgrep_target}" || true
  echo "killed." >> ${logfile}
}

monitor() {
  echo $(date) monitor start

  if [ ! -e ${logfile} ]; then
    echo $(date) "log file ${logfile} does not exist."
    echo $(date) "trying to start application."
    stop
    start
  else
    last_modified=$(date -r ${logfile} +%s)
    current=$(date +%s)

    if [ $((${last_modified} + ${monitor_threshold})) -lt ${current} ]
    then
      echo $(date) "log file ${logfile} has not been updated for ${monitor_threshold} seconds."
      echo $(date) "trying to restart application."
      stop
      start
    fi
  fi

  echo $(date) monitor end
}

cd ${basedir}

if [ -e ${customenv} ]; then
    source ${customenv}
fi

case "$1" in
  start)
    stop
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  monitor)
    monitor
    ;;
  *)
    echo $"Usage: ${0} {start|stop|restart|monitor}"
    exit 1
esac
