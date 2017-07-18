#!/bin/bash
path=$PWD

log_date=$1
access_log_path="/cache/logs/heka-data/$log_date"
count_log_path="/cache/logs/data_to_ftp/$log_date"

let A=$1%100

if [ $A -lt 10 ]
then

A="0$A"

fi

if [ $# -gt 1  ]
then
echo
hostname='live.mfniu.com'
echo "$hostname"
echo
echo "计数器"

cd $count_log_path
for file in `ls $log_date*`
do
    if echo $file | grep "${log_date}0000" &>/dev/null
    then
        continue
    fi
    echo `echo $file | cut -d '.' -f 1`    `awk -v count=0 '$2 ~ /live.mfniu.com/{count=count+$6}END{print count}' $file`
done

echo
echo "日志"

cd $access_log_path
file=`ls $log_date*`
if echo "$file" | grep 'gz$' &> /dev/null
then
    zegrep "\[$A.*$hostname .* (play|publish) " $file | awk '{split($3,TIME,":");mark=(TIME[2]*60+TIME[3]);count=mark+5-mark%5;HOST[count]=HOST[count]+$15}END{for(i in HOST){printf "'${log_date}'%02d",int(i/60);printf "%02d ",i%60;print HOST[i]}}' | sort -k 1
else
    egrep "\[$A.*$hostname .* (play|publish) " $file | awk '{split($3,TIME,":");mark=(TIME[2]*60+TIME[3]);count=mark+5-mark%5;HOST[count]=HOST[count]+$15}END{for(i in HOST){printf "'${log_date}'%02d",int(i/60);printf "%02d ",i%60;print HOST[i]}}' | sort -k 1
fi

else

echo
echo "总量"
echo
echo "计数器"

cd $count_log_path
for file in `ls $log_date*`
do
    if echo $file | grep "${log_date}0000" &>/dev/null
    then
        continue
    fi
    echo `echo $file | cut -d '.' -f 1`    `awk -v count=0 '{count=count+$6}END{print count}' $file`
done

echo
echo "日志"

cd $access_log_path
file=`ls $log_date*`
if echo "$file" | grep 'gz$' &> /dev/null
then
    zegrep "\[$A.* (play|publish) " $file | awk '{split($3,TIME,":");mark=(TIME[2]*60+TIME[3]);count=mark+5-mark%5;HOST[count]=HOST[count]+$15}END{for(i in HOST){printf "'${log_date}'%02d",int(i/60);printf "%02d ",i%60;print HOST[i]}}' | sort -k 1
else
    egrep "\[$A.* (play|publish) " $file | awk '{split($3,TIME,":");mark=(TIME[2]*60+TIME[3]);count=mark+5-mark%5;HOST[count]=HOST[count]+$15}END{for(i in HOST){printf "'${log_date}'%02d",int(i/60);printf "%02d ",i%60;print HOST[i]}}' | sort -k 1
fi

fi

cd $path
