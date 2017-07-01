#!/usr/bin/env python

'''
Modfuzz : Simple command line Modbus Client

Author: Sachin Parekh

Email: sachin.parekh1811@gmail.com
'''

import argparse
import socket
import struct
import sys


def get_args():
    parser = argparse.ArgumentParser(usage="Modfuzz.py [-r][-w] [optional] IP",description="Tool used to Read/Write data from/to Modbus Server")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--read" , help="Read register values", action="store_true")
    group.add_argument("-w", "--write",type=int, help="Write Coil value")
    parser.add_argument("-a","--address", type=int, default=0, help="Register address to be accessed or fetched")
    parser.add_argument("-u","--unit-identifier", type=int, default=1, help="Unit Identifier of the modbus device")
    parser.add_argument("-n", type=int, default=1, help="Number of registers to be read", dest="Num")
    parser.add_argument("-p","--port", type=int, default=502, help="Modbus port number ")
    parser.add_argument("IP", type=str, help="IP address of the Modbus Server")
    parser.parse_args()
    args = parser.parse_args()
    return(args)


def write_coil():
    try:
        unitId = args.unit_identifier 						
        functionCode = 6 						# function code = 6 for Write single register
        coilId = args.address
        val = args.write						
        req = struct.pack('!10BH', 0x18, 0x11, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), int(val))
        sock.send(req)
        rec = sock.recv(BUFFER_SIZE)
        print("Writen!")
     
    finally:
        sock.close()
        sys.exit()

def read_registers():
    try:
        num = args.Num
        byteformat = '!'+str(num)+'h'
        unitId = args.unit_identifier
        refnum = args.address        
        functionCode = 4
        req = struct.pack('!10BH', 0x18, 0x11, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(refnum), int(num))
        sock.send(req)
        rec = sock.recv(BUFFER_SIZE)
        a=list(rec)
        data=a[9:]
        try:
            data=''.join(data)
            intdata=struct.unpack(byteformat,data)
            for i in range(num):
                print('Register '+str(refnum+i)+': '+str(intdata[i]))
        except Exception:
            print("Error reading values. Try again")
            sock.close()
            sys.exit()

    finally:
        sock.close()
        sys.exit()

if __name__ == '__main__':
    
    #Get command line arguments
    args=get_args()

    # Create a TCP/IP socket
    TCP_IP = str(args.IP)         #Server IP 
    TCP_PORT = args.port          #Modbus port
    BUFFER_SIZE = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))

    if(args.read):
        read_registers()
    else:
        write_coil()