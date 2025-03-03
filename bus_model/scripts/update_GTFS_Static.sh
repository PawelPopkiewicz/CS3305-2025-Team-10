#!/bin/bash

PROJECT_ROOT=$(pwd | sed 's|bus_model/.*|bus_model/|' )

cd ${PROJECT_ROOT}/GTFS_Static/

wget https://www.transportforireland.ie/transitData/Data/GTFS_Realtime.zip

rm source_text_files/*.txt -f

unzip -d source_text_files/ GTFS_Realtime.zip 

rm GTFS_Realtime.zip*
rm gtfsr.db
cp chosen_routes.txt source_text_files/chosen_routes.txt

cd ${PROJECT_ROOT}

python3 -m GTFS_Static.create_db

echo "Created the gtfsr.db"
