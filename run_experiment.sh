#!/bin/sh
for i in {1..20}
do
    for ratio in 0 .1 .2 .3 .4 .5 .6 .7 .8 .9 1.0
    do
        rm zookeeper.db;
        ~/anaconda/bin/python zookeeper_server.py &> log_$1.log &
        sleep 1;
        ~/anaconda/bin/python experiment.py $ratio | tee -a log_exp_$1.log &&
        kill $(jobs -pr);
    done
    trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT;
done
printf \\a
