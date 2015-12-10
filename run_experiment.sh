#!/bin/sh

for ratio in 0 .25 .5 .75 1.0
do
    rm zookeeper.db;
    ~/anaconda/bin/python zookeeper_server.py &> log_$1.log &
    sleep 1;
    ~/anaconda/bin/python experiment.py $2 | tee -a log_exp_$1.log &&
    trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT;
done
printf \\a
