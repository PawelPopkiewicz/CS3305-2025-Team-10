#!/bin/bash/

PROJECT_ROOT=$(pwd | sed 's|bustimes_model/.*|bustimes_mode/|' )

cd ${PROJECT_ROOT}

python3 -m GTFS_Realtime.fetch_and_store

echo "fetched and stored the vehicle updates"
