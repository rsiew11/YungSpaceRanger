#!/usr/bin/python


import smbus
import sys
import getopt
import time
import pigpio


i2c_bus = smbus.SMBus(1)
OMRON_1 = 0x0A
OMRON_BUFFER_LENGTH = 35
temperature_data = [0]*OMRON_BUFFER_LENGTH

pi = pigpio.pi()

handle = pi.i2c_open(1,0x0a)

#initialize the device
result = i2c_bus.write_byte(OMRON_1,0x4C)


(bytes_read, temperature_data) = pi.i2c_read_device(handle,len(temperature_data))

print 'bytes read = ' + str(bytes_read)
print 'Data = '

PTAT = temperature_data[0] + temperature_data[1]*256
tP = [0]*16
index = 0
for i in xrange(2,bytes_read-2,2):
    tP[index] = temperature_data[i] + temperature_data[i+1]*256
    index+=1

tPEC = temperature_data[34]

for i in xrange(16):
    tP[i] = tP[i]*0.1
    print tP[i]




fo = open('/home/pi/YungSpaceRanger/hardware/packet/thermalData.txt',"w")
fo.write(str(tP)+"\n")








pi.i2c_close(handle)
pi.stop()

