#!/usr/bin/python

import socket
import os
import time

h = "localhost"
p = 9990
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((h, p))

while 1:
    cmd = raw_input("please input your command:")
    s.send(cmd)
    received_data = s.recv(8096)


    print "Received from server:", received_data
s.close()
