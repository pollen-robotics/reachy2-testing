#!/bin/bash
cd /home/prod/dev/orbita3d_testbench
#echo "Files will be stored to ~/Desktop/AssemblyTest/Orbita3d/" 
read -p "Please enter the complete file path (mouse select the file, right click copy and right click paste here): " NAME

cd scripts
python plot_test_data.py "$NAME"
read -p "ENTER to quit" _
