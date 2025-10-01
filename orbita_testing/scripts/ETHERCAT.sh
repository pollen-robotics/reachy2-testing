#!/bin/bash
printf "Starting Ethercat Master\n"
sudo ethercatctl start
printf "Detected Graph:\n"
ethercat graph
printf "Detected slaves:\n"
ethercat slaves
read -p "ENTER to quit" _
