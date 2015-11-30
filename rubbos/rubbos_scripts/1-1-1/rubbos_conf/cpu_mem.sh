#!/bin/bash

cd /bottlenecks/rubbos/rubbos_scripts/1-1-1
source set_bottlenecks_rubbos_env.sh
cd -

# delay inbetween snapshots

delay=1

# central host to send results to
analysis_host=$BENCHMARK_HOST

# monitoring start/end time in format YYYYmmddHHMMSS (20050920152059)
start_time=$1
end_time=$2

# data filename suffix
data_filename_suffix="`hostname`-${start_time}.data"

# sar filename
sar_filename=$RUBBOS_APP/sar-${data_filename_suffix}

# iostat filename
iostat_filename=$RUBBOS_APP/iostat-${data_filename_suffix}

# ps filename
ps_filename=$RUBBOS_APP/ps-${data_filename_suffix}

# date command in predefined format
date_cmd="date +%Y%m%d%H%M%S"
date=`$date_cmd`

# TEST MODE: start_time will be 2 seconds from launch, end time 5 seconds
#start_time=`expr $date \+ 2`
#end_time=`expr $date \+ 5`

#echo
#echo Current timestamp:  $date
#echo Start timestamp:  $start_time
#echo End timestamp:  $end_time
#echo

# make sure they have all arguments
if [ "$end_time" = "" ]; then
  echo usage: $0 \<delay\> \<analysis host\> \<start time\> \<end time\>
  echo start_time and end_time are in YYYYmmddHHMMSS format
  echo ie: 9/30/2005, 2:31:54pm = 20050930143154
  echo
  exit
fi

# wait until start time
#echo -n Waiting until start time \(${start_time}\)..
date=`$date_cmd`
while [ $date -lt $start_time ]; do
  sleep 1
  date=`$date_cmd`
done
#echo


# launch iostat
sudo nice -n -1 $SYSSTAT_HOME/bin/iostat -dxtk $delay > ${iostat_filename} &
iostat_pid=$!


# run test until end time
#echo -n Running test until end time \(${end_time}\)..
while [ $date -lt $end_time ]; do

  sleep $delay
  date=`$date_cmd`
done
#echo


# kill iostat
sudo kill -9 $iostat_pid


# chmod

sudo chmod g+w ${iostat_filename}
sudo chmod o+r ${iostat_filename}


# send data to analysis host
#echo Sending data to analysis host.. 
#scp -o StrictHostKeyChecking=no -o BatchMode=yes ${sar_filename} ${analysis_host}:/tmp/elba/rubbos
#scp -o StrictHostKeyChecking=no -o BatchMode=yes ${ps_filename} ${analysis_host}:/tmp/elba/rubbos

