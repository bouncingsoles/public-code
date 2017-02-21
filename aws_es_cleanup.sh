#!/bin/sh

###Set the cron to run daily, it will delete the logs that are older than X on that day.  

#Type the prefix of your indicies with spaces you want to clean
array=( )
#Delete index older than X days
daystodelete=14
esurl="http://aws-es-url/"

year=$(date --date="$daystodelete days ago" +"%Y")
month=$(date --date="$daystodelete days ago" +"%m")
day=$(date --date="$daystodelete days ago" +"%d")

for i in "${array[@]}"
do
	curl -XDELETE "$esurl$i-$year.$month.$day"
done
