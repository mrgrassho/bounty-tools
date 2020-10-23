#!/usr/bin/env bash

OUT="out"
OUT_BRUTE="out-brute"
WORDLIST=$2
if [[ $# -ge 1 ]]; then
    subs.py $1 | tee -a $OUT   
    cat $OUT | grep "*" | sed 's/\*\.//g' > aux
    cat $OUT | grep -v "*" >> aux
    mv aux $OUT 
    cat $OUT | xargs -I {} sh -c "cat $WORDLIST | sub-brute.sh {}" | tee -a $OUT_BRUTE
else
  echo " Usage: subs.sh TARGET_URL WORDLIST"
  echo ""
  echo " Examples:"
  echo "     subs.sh tesla.com words_alpha.txt"
fi


