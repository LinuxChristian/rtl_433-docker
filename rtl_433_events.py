#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import collections
import json
import os

import numpy as np
import paho.mqtt.publish as publish

from utils import *

rtl_devices = [12, 50, 29]

level = 0 # 8000 default, 0 auto
sleep_time = 0.1

# Custom hash for outdoor sensor
outdoor_conditions = ['98a99d53dba2239f8b6214764b025fac', None, None, None]
    
config = {
        'host': os.environ['mqtt_ip'],
        'port':os.environ['mqtt_port'],
        'command': ['/usr/local/bin/rtl_433', '-F', 'json'] + ['-R {}'.format(d) for d in rtl_devices] + ['-l {}'.format(level)],
        'debug': True,
}

if os.environ['mqtt_pass'] != 'password':
        config['password'] = os.environ['mqtt_pass']


def on_connect(mosq, obj, rc):
        print("rc: " + str(rc))

def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))

def on_message(mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# 6.116441 7.591386 240.7263 0.083% -20...+50 Celcius
A = 6.116441
m = 7.591386
Tn = 240.7263

def vapour_saturation_pressure(T):
    return A*10**(m*T/(T+Tn))

def absolute_humidity(T, RH):
    Pw = 100.0*vapour_saturation_pressure(T)*RH # Pa
    return 2.16679*Pw/(273.15 + T) # g/m3

def dew_point(T,RH):
    Pw = vapour_saturation_pressure(T)*RH
    return Tn/((m/np.log10(Pw/A)-1))

#api = remote.API(config['host'], config['password'], port=config['port'])
#api = remote.API(config['host'], port=config['port'])

#mqttc = mosquitto.Mosquitto()
#mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
#mqttc.on_message = on_message

def process_events(events):
    global outdoor_conditions
    events = uniqify(events) # Make events unique maintaining order
    for e in events:
        try:
            event = json.loads(e)
            if 'channel' in event:
                    device_id = "{}{}{}".format(event['model'], event['id'], event['channel'])
            elif 'unit' in event:
                    device_id = "{}{}{}".format(event['model'], event['id'], event['unit'])
#                    print('unit: {}'.format(unit))
            else:
                    device_id = "{}{}".format(event['model'], event['id'])
            event_id = hash_string(e.encode())
        except ValueError:
            print("WARNING: Received non-json data from rtl_433: {}".format(e))
            continue
        qos = 2
        retain = 1
        msgs = []
        if "Weather Sensor THGR810" == event['model']:
                T  = event['temperature_C']
                RH = event['humidity']/100.0
                event['dew_point'] = dew_point(T, RH)
                event['absolute_humidity'] = absolute_humidity(T, RH)

                # Special case with outdoor sensor
                if outdoor_conditions[0] == hash_string(device_id.encode()):
                        outdoor_conditions[1] = T
                        outdoor_conditions[2] = RH
                        outdoor_conditions[3] = event['absolute_humidity']
                elif outdoor_conditions[1] is not None:
                        # Append extra info if avaiable
                        event['outdoor_temp_diff'] = T - outdoor_conditions[1]
                        event['outdoor_abs_diff'] = event['absolute_humidity'] - outdoor_conditions[3]
                        event['outdoor_rel_diff'] = (RH - outdoor_conditions[2])*100
                else:
                        # Append extra info if avaiable
                        event['outdoor_temp_diff'] = 0
                        event['outdoor_abs_diff'] = 0
                        event['outdoor_rel_diff'] = 0

        msgs.append(("rtl433/{}".format(hash_string(device_id.encode())), json.dumps(event), qos, retain))
        publish.multiple(msgs, hostname="localhost", protocol=4)
#        mqttc.publish("rtl433/" + hash_string(device_id.encode()), e, protocol = 4)
#        remote.set_state(api, 'sensor.rtl_433_' + hash_string(device_id.encode()), new_state=event['state'], attributes=event)

        if config['debug']:
            print("INFO: {}/{}: {}".format(event_id, hash_string(device_id.encode()), event))


if __name__ == '__main__':
    print("INFO: Starting command: {}".format(config['command']))
    startsubprocess(config['command'], process_events, sleep_time=sleep_time)
