#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: Andre

class FMS:
    name=''
    mqtt_addr=''
    mqtt_port=0

    aalp_addr=''
    aalp_port=0

    def __init__(self, name, mqtt_addr, mqtt_port, aalp_addr, aalp_port):
        self.name = name
        self.mqtt_addr = mqtt_addr
        self.mqtt_port = mqtt_port
        self.aalp_addr = aalp_addr
        self.aalp_port = aalp_port
    
class TOS:
    name=''
    addr=''
    port=0

    def __init__(self, name, addr, port):
        self.name = name
        self.addr = addr
        self.port = port

def main():
    #-----------------------------------------
    FMS_A=FMS("FMS_A", "172.28.129.196", 30845, "172.28.138.55", )
    FMS_B=FMS("FMS_B", "172.29.60.11",   1883,  "172.29.60.11, 6000)

    TOS_1=TOS("TOS_1", "10.160.7.113", 1521)
    TOS_2=TOS("TOS_2", "10.160.21.87", 1521)

if __name__ == "__main__":
    main()
