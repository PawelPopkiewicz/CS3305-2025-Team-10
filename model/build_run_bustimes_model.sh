#!/bin/bash

docker build -t bustimes_model .

docker run -p 5000:5000 bustimes_model

