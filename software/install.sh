#!/bin/bash
command=$1

if [ "$command" = "install" ]; then
    echo "installing necesary packages"
    sudo apt update
    sudo apt install ros-melodic-desktop-full
    pip install face-recognition 
    sudo apt install ros-melodic-usb-cam
    sudo apt install ros-melodic-people-msgs
else
    echo "excecuting necesary things"
    roslaunch usb_cam usb_cam-test.launch
fi
