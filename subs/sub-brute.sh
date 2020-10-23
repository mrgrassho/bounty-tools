#!/bin/bash 

domain=$1
while read sub; do
    data=$(echo "$sub.$domain" | httprobe)
    if [[ ! -z "$data" ]]; then 
        echo "${data/ /\n}"
    fi
done