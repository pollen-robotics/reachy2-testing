#!/bin/bash

cd /home/prod/dev/poulpe_ethercat_controller
read -p 'Which Orbita2d is it? 1=LeftShoulder 2=LeftElbow 3=RightShoulder 4=RightElbow: ' ORBITA
case $ORBITA in

  1)
      printf "Left Shoulder\n"
      ESI="LeftShoulderOrbita2d.bin"
      ;;

  2)
      printf "Left Elbow\n"
      ESI="LeftElbowOrbita2d.bin"
      ;;

  3)
      printf "Right Shoulder\n"
      ESI="RightShoulderOrbita2d.bin"
      ;;
  
  4)
      printf "Right Elbow\n"
      ESI="RightElbowOrbita2d.bin"
      ;;

  *)
      read -p "Error! unknown (ENTER to quit)" _
      exit 1
      ;;
esac

CMD="ethercat sii_write -p0 /home/prod/dev/poulpe_ethercat_controller/config/esi/reachy2/firmware1.5/$ESI"
echo $CMD
bash -c "ethercat sii_write -p0 /home/prod/dev/poulpe_ethercat_controller/config/esi/reachy2/firmware1.5/$ESI"


echo "POWER CYCLE THE DEVICE AFTER THIS STEP!!!"

read -p "ENTER to quit" _
