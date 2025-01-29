#!/bin/bash/

wget https://www.transportforireland.ie/transitData/Data/GTFS_Realtime.zip

unzip -d source_text_files/ GTFS_Realtime.zip 

rm GTFS_Realtime.zip

python3 create_db.py

