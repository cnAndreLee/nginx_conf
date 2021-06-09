#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: Andre

import docker
import time
import os

class FMS:
    name=''
    mqtt_ip=''
    mqtt_port=0

    aalp_ip=''
    aalp_port=0

    def __init__(self, name, mqtt_ip, mqtt_port, aalp_ip, aalp_port):
        self.name = name
        self.mqtt_ip = mqtt_ip
        self.mqtt_port = mqtt_port
        self.aalp_ip = aalp_ip
        self.aalp_port = aalp_port
        self.show()

    def show(self):
        print("name:"+self.name+"  mqtt:"+self.mqtt_ip+":"+str(self.mqtt_port)+"  aalp:"+self.aalp_ip+":"+str(self.aalp_port))
    
class TOS:
    name=''
    ip=''
    port=0

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.show()

    def show(self):
        print("name:"+self.name+"  addr:"+self.ip+":"+str(self.port))
    
def generate_nginx_conf(listen_port, ip, port):
    nginx_conf = '''
events {{
    worker_connections 1024;
    # multi_accept on;
}}

stream {{

    server {{
        listen {listen_port} so_keepalive=on;
        proxy_pass {ip}:{port};
    }}
}}
    '''.format(listen_port=listen_port, ip=ip, port=port)
    if DEBUG==True:
        print("\n\n===============================\nthe nginx.conf is \n{}\n========================================".format(nginx_conf))
    return nginx_conf

def setactproxy():

    actStr=input("Please input the carid array you want to set, use spaces to spearate, such as '11 31 32', the range is 1-99 :\n")
    try:
        actArray = list(set([int(n) for n in actStr.split()]))
    except:
        print("input error")
        exit()

    finnalActArray=[]
    for index in range(len(actArray)):
        if actArray[index] > 0 and actArray[index] < 100:
            finnalActArray.append(actArray[index])
        else:
            print("car id {} is out of range! Deleted for you!".format(actArray[index]))

    if len(finnalActArray) == 0:
        print("list is empty")
        exit()
    elif len(finnalActArray) == 1:
        print("\n**************\n  the car will be set is {}\n**************".format(finnalActArray[0]))
    else:
        print("\n**************\n  the cars will be set are {}\n**************".format(finnalActArray))

    portlist=[]
    for n in finnalActArray:
        portlist.append(n+7000)

    if DEBUG==True:
        print("portlist is {}".format(portlist))

    while 1:
        fmsStr=input("Now, input the FMS which you want cars to connect , such as A or B:\n")

        #if fmsStr=='A' or fmsStr=='a':
        #    fmsStr='A'
        #    break
        #elif fmsStr=='B' or fmsStr=='b':
        #    fmsStr='B'
        #    break
        if fmsStr in FMS_DICT:
            break
        else:
            print("Input error !!!")

    client = docker.from_env()
    apiClient = docker.APIClient(base_url='unix://var/run/docker.sock')

    # start
    for index in range(len(portlist)):
        NginxConf=generate_nginx_conf(portlist[index], FMS_DICT[fmsStr].mqtt_ip, FMS_DICT[fmsStr].mqtt_port )

        with open(TMP_FILENAME, 'w') as f:
            f.write(NginxConf)
        #f=open(TMP_FILENAME, 'w')
        #f.write(NginxConf)
        #f.close()

        first_name="ACT_A{}_".format(str(portlist[index])[1:4])
        name=first_name+fmsStr
        if DEBUG:
            print("first_name is "+first_name)

        #cmd="docker stop {0}A {0}B ; docker rm {0}A {0}B".format(first_name)
        #if DEBUG:
        #    print("CMD is "+cmd)

        #run cmd
        for key in FMS_DICT:
            print("deleting container < "+first_name+key+" >")
            try:
                apiClient.stop(first_name+key)
                apiClient.remove_container(first_name+key)
            except docker.errors.NotFound:
                pass


        #cmd="docker run -d --name {0} --restart=always -p 0.0.0.0:{1}:{1}/tcp -v {2}:/etc/nginx/nginx.conf:ro nginx:latest".format(name, portlist[index], TMP_FILENAME)
        #if DEBUG:
        #    print("runCMD is "+cmd)

        print(client.containers.run('nginx:latest', detach=True, name=name, restart_policy={"Name": "always"}, ports={str(portlist[index])+'/tcp':('0.0.0.0', portlist[index])}, volumes={TMP_FILENAME:{'bind':'/etc/nginx/nginx.conf', 'mode': 'ro'}}))

        time.sleep(2)

    #rm tmpfile
    if DEBUG==False:
        os.remove(TMP_FILENAME)

    client.close()
    apiClient.close()


DEBUG=False
TMP_FILENAME="/tmp/nginx_tmp.conf"

print("-----------------------------------------")
FMS_DICT={'A':FMS("FMS_A", "172.28.129.196", 30845, "172.28.138.55", 5000), 'B': FMS("FMS_B", "172.29.60.11",   1883,  "172.29.60.11",  6000)}

TOS_DICT={'1': TOS("TOS_1", "10.160.7.113", 1521), '2': TOS("TOS_2", "10.160.21.87", 1521)}
print("----------------------------------------\n")

def main():
   
    #client = docker.from_env()
    #print(client.containers.list())
    #print(type(client.containers.list()))
    #print(type(client.containers.list()[0]))

    # selector=input("Please input the system which you want to operate, 'TOS', 'XJD', 'XCC' or 'ACT' ")

    setactproxy()



if __name__ == "__main__":
    main()
