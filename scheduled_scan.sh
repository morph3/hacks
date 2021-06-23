#!/bin/bash
display_usage() { 
	echo "This script expects a list of subdomains to scan, second argument is the time in minutes ." 
	echo -e "\nUsage: $0 [arguments] \n" 
} 
# if less than two arguments supplied, display usage 
	if [  $# -le 1 ] 
	then 
		display_usage
		exit 1
	fi 


input=$1
while IFS= read -r line
do
	python3 /opt/sectumsempra/sectumsempra.py all -d $line -m full
	sleep `expr 60*\$2`

done < "$input"

