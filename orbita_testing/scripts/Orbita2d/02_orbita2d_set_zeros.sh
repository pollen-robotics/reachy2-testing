#!/bin/bash

read -p 'Did you set the Obita2d in the zero position? [y/N]' SHOULD_FLASH
case $SHOULD_FLASH in
  "y"|"Y")
        printf "YES\n"
        . /home/prod/.bashrc
        echo "Flashing bootloader"
        cd /home/prod/dev/bootloader_Poulpe
        cargo flash --release --chip STM32H743VGTx
        echo "Zeros firmware program"
        cd /home/prod/dev/firmware_Poulpe
        DEFMT_LOG=debug cargo run --release --features=orbita2d_pvt --bin bench_Orbita2dWriteZeros
        read -p "ENTER to quit" _
        ;;
  *) 
        printf "NO\n"
        exit 1
        ;;
esac

read -p "ENTER to quit" _
