#!/bin/bash

cd ~/dev/poulpe_ethercat_controller/poulpe_ethercat_grpc
ETHERCAT_PATH=/home/prod/dev/ethercat cargo run --example=get_bus_state -- --configfile ethercat.yaml --start-server
read -p "ENTER to quit" _
