#!/bin/bash

COOKIES_FILE=adventofcode.com_cookies.txt

if ! test -d input;
then
  # create input dir
  mkdir input
fi

for i_without_leading in {1..25};
do
  i_with_leading=$(printf "%02d" $i_without_leading)

  if [[ "2024-12-10#$i_with_leading" -lt $(date +%Y-%_m-%_d) ]];
  then
      # this date is yet to come
      break
  fi

  if ! test -f "input/$i_with_leading.txt"; then
    # download input file
    wget --load-cookies=$COOKIES_FILE https://adventofcode.com/2024/day/$i_without_leading/input -O input/$i_with_leading.txt
  fi

done
