#!/bin/bash

cd /home/prod/dev/poulpe_ethercat_controller
read -p 'Which Orbita3d is it? 1=Neck 2=LeftWrist 3=RightWrist : ' ORBITA
case $ORBITA in

  1)
      printf "Neck\n"
      ESI="NeckOrbita3d.bin"
      ;;

  2)
      printf "Left Wrist\n"
      ESI="LeftWristOrbita3d.bin"
      ;;

  3)
      printf "Right Wrist\n"
      ESI="RightWristOrbita3d.bin"
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
