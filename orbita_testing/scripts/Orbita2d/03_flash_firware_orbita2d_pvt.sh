#!/bin/bash
. /home/prod/.bashrc
echo "Flashing bootloader"
cd /home/prod/dev/bootloader_Poulpe
cargo flash --release --chip STM32H743VGTx
echo "Flashing firmware"
cd /home/prod/dev/firmware_Poulpe
DEFMT_LOG=off cargo run --release --features=orbita2d_pvt
read -p "ENTER to quit" _
