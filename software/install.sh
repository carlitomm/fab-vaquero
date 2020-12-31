#!/bin/bash

sudo apt update
sudo apt install ros-melodic-desktop-full
pip install face-recognition #100mb
sudo apt install ros-melodic-usb-cam #1Kb
roslaunch usb_cam usb_cam-test.launch