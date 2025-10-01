#!/bin/bash

cd /home/prod/dev/orbita2d_control/orbita2d_controller
. /home/prod/.bashrc
ETHERCAT_PATH=/home/prod/dev/ethercat RUST_LOG=info cargo run --example=poulpe2d -- --configfile config/ethercat_poulpe.yaml --start-server
read -p "ENTER to quit" _
