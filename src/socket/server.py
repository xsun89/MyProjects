#!/usr/bin/python

import socket
import os
import time

h = 'localhost'
p = 9990
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((h, p))
s.listen(1)
(conn, addr) = s.accept()
print "get connection from ", addr
while 1:
    data = conn.recv(4096)
    if not data:
        time.sleep(1.5)
    cmd = os.popen(data)
    result = cmd.read()

    conn.sendall(result)
conn.close()
