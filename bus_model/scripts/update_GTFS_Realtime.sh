#!/bin/bash/

PROJECT_ROOT=$(pwd | sed 's|bus_model/.*|bus_model/|' )

cd ${PROJECT_ROOT}/GTFS_Realtime/

python3 -m GTFS_Realtime.update_model

echo "Fetched and stored the vehicle updates"