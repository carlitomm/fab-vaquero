#!/bin/bash
command=$1

if [ "$command" = "install" ]; then
    echo "installing necesary packages"
    sudo apt update
    sudo apt install ros-melodic-desktop-full
    pip install face-recognition 
    sudo apt install ros-melodic-usb-cam
    sudo apt install ros-melodic-people-msgs
elif [ "$command" = "installtensor" ];then
    pip install virtualenv 
    pip install facenet_pytorch #770mg
    pip install tensorflow      #300mg
    pip install python-opencv
    pip install mtcnn
else
    echo "excecuting necesary things"
    roslaunch usb_cam usb_cam-test.launch
    cd /media/carlos/Datos/documents/PROYECTOS/fabelo/vaquero/repo-vaquero || exit
    cd software || exit
    python node.py
    #python ardu_comm.py
fi
