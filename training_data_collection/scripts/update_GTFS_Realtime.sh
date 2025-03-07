#!/bin/bash

PROJECT_ROOT=$(pwd | sed 's|training_data_collection/.*|training_data_collection/|' )

cd ${PROJECT_ROOT}

python3 -m GTFS_Realtime.fetch_store

echo "fetched and stored the vehicle updates"
