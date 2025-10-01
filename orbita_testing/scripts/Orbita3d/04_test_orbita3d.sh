#!/bin/bash
cd /home/prod/dev/orbita3d_control/orbita3d_controller
ETHERCAT_PATH=/home/prod/dev/ethercat RUST_LOG=info cargo run --example=poulpe3d -- --configfile config/ethercat_poulpe.yaml --start-server
read -p "ENTER to quit" _
