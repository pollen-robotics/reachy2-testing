#!/bin/bash

read -p "Orbita2d serial number: " serialnb
outfile="O2D_"$serialnb"_breakin.csv"
echo $outfile

mkdir /home/prod/Desktop/AssemblyTest/Orbita2d/$serialnb

cd /home/prod/dev/orbita2d_testbench
. /home/prod/.bashrc
ETHERCAT_PATH=/home/prod/dev/ethercat RUST_LOG=info cargo run --release -- --start-server --configfile=config/ethercat_poulpe.yaml --input-csv=scripts/test_breakin_input.csv --output-csv=/home/prod/Desktop/AssemblyTest/Orbita2d/$serialnb/$outfile --nb-loop=10

read -p "ENTER to quit" _
