#!/bin/sh
spin[0]="-"
spin[1]="\\"
spin[2]="|"
spin[3]="/"
mkdir ./route53

#ALl domains
list=( $(./cli53 l | grep Name | cut -f2 -d\" | sed 's/\.$//g') )

echo -e "This script is going to dump every record in Route53 to a file."
echo -e "Press enter to continue or CTRL-C to exit."
read y

for i in "${list[@]}"
do
#Run the command one one time per record but get different parts of the output
output=`./cli53 export $i`
#Use quotes so you don't lose linebreaks in output, this is needed for AWK to work.
echo "$output"

#dnsname=`cat $output | head -1 | awk '{print $2}'`
echo $i
echo "$output" > ./route53/$i.txt

sleep 0.5
#./cli53 export $i &>> route53info.txt
##Spinning logo and to slow it down a bit while we build the file
for i in "${spin[@]}"
  do
        echo -ne "\b$i"
        sleep 0.1
  done
done
