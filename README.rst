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


Attaching the dongle
 * Find the RTL-SDR dongle usb bus address

.. code-block:: bash
    #~ lsusb
    .
    .
    Bus 003 Device 006: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T
    .
    .
    
    docker run -d --name rtl_433 --device=/dev/bus/usb/003/006 -e MQTT_IP='10.0.0.1' rtl_433

The following environmental variables are available,

+-----------------------+-----------------------------------------------------+
| Name                  | Description                                         |
+=======================+=====================================================+
| MQTT_IP               | IP address of MQTT server.                          |
|                       | Default: 127.0.0.1                                  |
+-----------------------+-----------------------------------------------------+
| MQTT_PASS             | Password for  MQTT server.                          |
|                       | Default: No password                                |
|                       | Format: {‘username’:”<usr>”,‘password’:”<pass>”}    |
+-----------------------+-----------------------------------------------------+
| MQTT_PORT             | Port of MQTT server.                                |
|                       | Default: 1883                                       |
+-----------------------+-----------------------------------------------------+
| MQTT_DEBUG            | Show debug inforation.                              |
|                       | Default: True                                       |
+-----------------------+-----------------------------------------------------+

Credits
========
MQTT event script largely inspired by work from @kajksa.
