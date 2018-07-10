#!/usr/bin/python
#-*- coding:UTF-8 -*-

import time

import RPi.GPIO as GPIO
 
#超声波引脚定义
EchoPin = 0
TrigPin = 1
 
#超声波引脚初始化
def init():
    #设置GPIO口为BCM编码方式
    GPIO.setmode(GPIO.BCM)
    #忽略警告信息
    GPIO.setwarnings(False)
    time.sleep(2)
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)

#超声波函数
def GetDistance():
    GPIO.output(TrigPin,GPIO.HIGH) # set port/pin value to 1/GPIO.HIGH/True
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW) # set port/pin value to 0/GPIO.LOW/False
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    timeDelta = t2 - t1
    distance = (timeDelta * 340 / 2) * 100
    #print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
    #print("time delta: %fs" %(timeDelta))
    time.sleep(0.01)
    return distance 

def main():
    print("### Distance Sensor Starts Working (in StandAlone mode) ###")
    try:
        init()
        time.sleep(2)
        distance = GetDistance()
        print(">>> distance is: %dcm" %distance)
    except KeyboardInterrupt:
        print("### Distance Sensor Ends ###")

    GPIO.cleanup()

if __name__ == '__main__':
    main()
