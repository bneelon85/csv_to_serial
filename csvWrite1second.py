# -*- coding: utf-8 -*-

# Import Libraries
import time
import serial
import datetime
import csv

ser = 0

#Initialize Serial Port
def serial_connection():
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600 # Baud Rate for serial port
    ser.port = "COM9" # Serial port to write to. On Windows COM<Number> on Linux ttyS<Number>

    #check to see if port is open or closed
    if (ser.isOpen() == False):
        #print ('The Port %d is Open ' + ser.portstr)
          #timeout in seconds
        ser.timeout = 1
        ser.open()

    else:
        print ('The Port %d is closed')

# File Path to CSV you'd like to stream
file_path = "serial_test.csv"

# Get number of rows in CSV
file = open(file_path)
reader = csv.reader(file)
lines= len(list(reader))

serial_connection()

while True:
    cnt  = 1 # Start at row 1
    if cnt <= lines: # Number of Rows in the CSV
        with open(file_path) as fp:
            line = fp.readline()
            while line:
                currentDT = str(datetime.datetime.now().replace(microsecond=0)) # Current System Time
                print(bytes(currentDT+","+line.strip()+',\r\n',encoding='utf-8')) # Print output to local console
                ser.write(bytes(currentDT+","+line.strip()+',\r\n',encoding='utf-8')) # Publish currentDT plus CSV row to serial port
                line = fp.readline() 
                cnt += 1 # Increment row by 1
                time.sleep(0.9995) # Sleep for 1 second before publishing next row to serial port
    else: # If end of file met, start again
        cnt = 1
        with open(file_path) as fp:
            line = fp.readline()
            while line:
                currentDT = str(datetime.datetime.now().replace(microsecond=0))
                print(bytes(currentDT+","+line.strip()+',\r\n',encoding='utf-8'))
                ser.write(bytes(currentDT+","+line.strip()+',\r\n',encoding='utf-8'))
                line = fp.readline()
                cnt += 1
                time.sleep(0.9995)
            
            