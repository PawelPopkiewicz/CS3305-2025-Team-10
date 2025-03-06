#!/bin/bash


echo "Starting to fetch vehicles"

curl http://127.0.0.1:5002/v1/update_realtime

echo "Fetched and stored the vehicle updates"