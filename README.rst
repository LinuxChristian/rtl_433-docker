# rtl_433-docker
A stateless container for the rtl_433 project

Usage
================
Standard build

 git clone https://github.com/LinuxChristian/rtl_433-docker.git
 cd rtl_433-docker/
 docker build -t rtl_433 .
 docker run -d --name rtl_433 -e mqtt_ip='10.0.0.1' -e mqtt_pass='password' -e mqtt_port='8123' rtl_433
