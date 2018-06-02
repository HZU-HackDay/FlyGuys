#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author homeway
# @Link http::homeway.me
# @Github https://github.com/grasses
# @Version 2018.06.03

import serial, json, syslog, time, sys

port = "/dev/tty.HC-06-SPPDev"
def main(port):
    ard = serial.Serial(port, 9600, timeout=1)
    send =""
    time.sleep(1.5)
    while (True):
        send = "Everything Ok, time={:d}\n".format(int(time.time()))
        ard.flush()
        send = str(send)
        # print("=> Python sent: {:s}".format(send))
        # ard.write(send)

        msg = ard.readline().strip('\n\r') #ard.read(ard.inWaiting()).strip('\n\r') 
        if msg != "":
            print ("<= From arduino: {:s}".format(msg))
        try:
            key = ["result","data"]
            value = msg.split("-",2)
            data = dict(zip(key,value))
        except:
            print "ERROR!"
        print msg
    else:
        print "Exiting"
    exit()

if __name__ == "__main__":
    try:
        main(sys.argv[1] if len(sys.argv) > 1 else port )
    except KeyboardInterrupt:
        ser.close()