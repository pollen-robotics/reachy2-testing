#!/bin/bash
. /home/prod/.bashrc
cd /home/prod/dev/arm_control/arm_controller
read -p "ENTER to move" _
RUST_LOG=info cargo run --example=test_arm_move -- --side left --configfile config/test_arm/left/test_left_arm.yaml
read -p "ENTER to quit" _
