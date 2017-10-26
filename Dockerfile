FROM debian:latest
MAINTAINER Christian Juncker Brædstrup <christian@junckerbraedstrup.dk>

WORKDIR /tmp/

RUN apt-get update
RUN apt-get install -y git libtool libusb-1.0.0-dev librtlsdr-dev rtl-sdr cmake automake python3 python3-pip
RUN pip3 install paho-mqtt numpy
RUN git clone https://github.com/merbanan/rtl_433.git

COPY build.sh .
COPY rtl_433_events.py .
COPY utils.py .

# Build rtl_433
RUN ./build.sh

# MQTT env variables
ENV mqtt_ip=192.168.1.100
ENV mqtt_pass=password
ENV mqtt_port=8123

CMD python3 rtl_433_events.py