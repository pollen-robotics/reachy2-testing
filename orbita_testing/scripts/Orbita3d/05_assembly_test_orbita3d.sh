#!/bin/bash
cd /home/prod/dev/orbita3d_testbench
echo "Files will be stored to ~/Desktop/AssemblyTest/Orbita3d/" 
read -p "Please enter the file name [ex. o3d_test.csv] " NAME
ETHERCAT_PATH=/home/prod/dev/ethercat RUST_LOG=info cargo run --release \
        -- --start-server --configfile=config/ethercat_poulpe.yaml \
        --input-csv="scripts/test_input.csv"\
        --output-csv="/home/prod/Desktop/AssemblyTest/Orbita3d/$NAME"

cd scripts
python plot_test_data.py "/home/prod/Desktop/AssemblyTest/Orbita3d/$NAME"
read -p "ENTER to quit" _
