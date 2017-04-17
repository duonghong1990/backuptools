#!bin/bash
echo 'start-'$(date -I)
echo $(pwd)
/usr/bin/python $(pwd)/drive.py
sleep 5;
echo 'end-'$(date -I)

