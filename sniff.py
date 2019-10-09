import serial
import sys
import struct


ser = serial.Serial('/dev/ttyUSB0', 230400)

sync=[b'\xde',b'\xad',b'\xbe',b'\xef']
crc=b'\xcc\xcc'
buf=[0,0,0,0]

SYS=7

def little_endian(data,len):
    if len == 2:
        return struct.unpack("<h", data)[0]
    if len == 4:
        return struct.unpack("<l", data)[0]

while True:
    buf.pop(0)
    buf.append(ser.read(1))
    if buf == sync:
        length = little_endian(ser.read(2),2)
        data = ser.read(length)
        timestamp = little_endian(data[2:6],4)

        #check for length error
        if data[-2:] != crc and data[1] != SYS:
            print(data)
            sys.exit()
        else:
            f = open("{0}.bin".format(timestamp),"wb")
            f.write(data)
            f.close
