#!/bin/bash

set -eu

#propmt the user to enter a filename
echo -n "enter the filename you want to check:"
read filename

#check to see if file exists and is a regular file
if [[ -f "$filename" ]]; then
	echo "$filename exists!"
else
	echo "$filename does not exist!"
fi
