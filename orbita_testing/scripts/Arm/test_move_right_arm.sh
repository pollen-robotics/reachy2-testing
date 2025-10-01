#!/bin/bash
. /home/prod/.bashrc
cd /home/prod/dev/arm_control/arm_controller
read -p "ENTER to move" _
RUST_LOG=info cargo run --example=test_arm_move -- --side right --configfile config/test_arm/right/test_right_arm.yaml
read -p "ENTER to quit" _
