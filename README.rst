rtl_433-docker
###############
A stateless container for hosting RTL software defined radio (SDR) projects. The container must have a SDR dongle attached. All signal that are received and decoded will be send over the MQTT (machine-to-machine) protocol to any devices listening.

Usage
================
Standard build

.. code-block:: bash

    git clone https://github.com/LinuxChristian/rtl_433-docker.git
    cd rtl_433-docker/
    docker build -t rtl_433 .
    docker run -d --name rtl_433 -e mqtt_ip='10.0.0.1' -e mqtt_pass='password' -e mqtt_port='8123' rtl_433

The following environmental variables are available,

+-----------------------+-----------------------------------------------------+
| Name                  | Description                                         |
+=======================+=====================================================+
| mqtt_ip               | IP address of MQTT server.                          |
+-----------------------+-----------------------------------------------------+
| mqtt_pass             | Password for  MQTT server.                          |
|                       | Default: 'password' means no password set           |
+-----------------------+-----------------------------------------------------+
| mqtt_port             | Port of MQTT server.                                |
+-----------------------+-----------------------------------------------------+

Credits
========
MQTT event script largely inspired by work from @kajksa.
