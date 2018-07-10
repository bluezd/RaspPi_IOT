#!/usr/bin/python
#-*- coding:UTF-8 -*-

import json
import random
import getopt
import requests
import subprocess
import re, sys, time

from ultrasonic.ultrasonic import Ultrasonic
 
def doUpdate(payload):
    url = 'http://heng-ge.cn:8080/coldChainLogistics/reportTemperatureLocation.do'
    #payload = {"channel":"xebestorderer","chaincode":"xebest","method":"insertTemandLoc","args":["goods_1234","kevins house","-4C","2018-7-4 11:55"],"chaincodeVer":"v1"}
    headers = {'content-type': 'application/json'}
    while True:
        response = requests.get(url, data=json.dumps(payload), headers=headers)
        if json.loads(response.text)["resultCode"] == "Success":
            return 0
        time.sleep(1)

def updateTem(tem=0):
    payload = {"temperature": str(tem), "locationId": mode}
    res = doUpdate(payload)
    if res == 0:
        print("--> Update Tem=%s Success in %s Mode" %(tem, mode))

def updateGPS():
    num = random.randint(1, 3)
    value = "GPS"+str(num)
    payload = {"locationId": mode}
    res = doUpdate(payload)
    if res == 0:
        print("--> Update %s Success in %s Mode" %(value, mode))

def getTemHum():
    """docstring for getTemHum"""
    regx = re.compile('\d+\.\d+')
    cmd = ['TEM_HUM', '-o']
    while True:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.wait()
        if not p.returncode:
            res = regx.findall(p.communicate()[0])
            return (res[0], res[1])
        time.sleep(1)

def updateTemInfinite():
    print("### TEM Sensor Starts Working (in %s mode) ###" %mode)
    try:
        while True:
            hum, tem = getTemHum()
            print("TEM: " +tem)
            updateTem(round(float(tem), 2))
            time.sleep(10)
    except KeyboardInterrupt:
        print("### TEM Sensor Ends ###")

def usage():
    """docstring for usage"""
    print """
Usage: %s 
        -m "CAR"      <car mode>
           "FREEZER1" <freezer1 mode>
           "FREEZER2" <freezer2 mode>
           "GPS"      <GPS mode>
    """ %sys.argv[0]
    sys.exit(2)

def main():
    try:
        ops, args = getopt.getopt(sys.argv[1:], "hm:", ["help", "mode="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    if len(args) != 0 or len(sys.argv) == 1:
        print("Invalid Options")
        usage()

    global mode
    mode=None
    for o, a in ops:
        if o in ('-m', '--mode'):
            mode = a.strip("=")
            if mode not in ("CAR", "FREEZER1", "FREEZER2", "GPS"):
                print("Invalid Options")
                usage()
        else:
            usage()

    if mode == "CAR":
        updateTemInfinite()
    else:
        print("### Distance Sensor Starts Working (in %s mode) ###" %mode)
        try:
            ultra = Ultrasonic()
            time.sleep(2)
            count=0
            while True:
                print("# Get Distance count %d:" %count)
                distance = ultra.GetDistance()
                print(">>> distance is: %dcm" %distance)
                if distance < 5:
                    if mode.startswith("FREEZER"):
                        hum, tem = getTemHum()
                        print("TEM: " +tem)
                        updateTem(round(float(tem), 2))
                    elif mode == "GPS":
                        updateGPS()
                    time.sleep(2)
                time.sleep(1)
                count+=1
        except KeyboardInterrupt:
            print("### Distance Sensor Ends ###")

        ultra.cleanup()

if __name__ == '__main__':
    main()
