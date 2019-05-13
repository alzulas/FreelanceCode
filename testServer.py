#Final Production Server

## Author: Leah Zulas, April 2019
## This program takes readings from a piz0 which is hosting the AMG88xx GridEye 8x8 sensor
## It opens a port for the pi0w to recieve data, as well as a connection with the postgres server on the linux server to deliver the data
## It checks the IP Of the various devices to know who is talking to it and what details to send
## It creates all the identifiers that are needed for the postgres server
## Then sends an insert statement to postgres to put the data in the table 

#!/usr/bin/env python

import socket
import matplotlib.pyplot as plt
import numpy as np
import json
import time
from datetime import datetime
import psycopg2

#Home devices information
homeID = "xxx"
device_reporting_22 = "AMG88xx_Grid_Eye"
device_location_22 = "Bedroom"
fileLocation = "/home/pi/UniqueIDIterator.txt"

#Connection open information
TCP_IP = 'xx.xx.xx.xx'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#Postgres information 
PGHOST="xx.xx.xx.xx"
PGDATABASE="testDataBase"
PGUSER="postgres"
PGPASSWORD="SomePassword"

#Port open to listen
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError as msg:
    s = None
    continue
try:
    s.bind((TCP_IP, TCP_PORT))
except OSError as msg:
    s.close()
    s = None
    continue
if s is None:
    print('Could not open socket')
    sys.exit(1)

# Set up a connection to the postgres server.
conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER +" password="+ PGPASSWORD
pg_conn=psycopg2.connect(conn_string)
print("Connected to postgres")

# Create a cursor object
cur = conn.cursor()

str1 = ""

#print ('Connection address:', addr)
while True:
    #Wait until data to retreive
    s.listen(1)
    conn, addr = s.accept()
    print ('Connection address: ', addr)
    while 1:
        #Receiveing data and decoding bytes
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        conn.send(data)  # echo
        str1 = data.decode("utf-8")
    #print("List of data: ")
    #print(str1)

    #Pulling new UniqueID for Postgres
    f = open(fileLocation, 'r+')
    UniqueID = f.read()
    UniqueID = int(UniqueID) + 1
    f.seek(0)
    f.write(str(UniqueID))
    f.truncate()
    f.close()

    #Determining what devices data we have, so as to fill in the right infor for feilds.
    if (addr[0] == 'xx.xx.xx.xx'): 
        identifiers = (str(UniqueID) + "," + homeID + "," + device_reporting_xx + "," + device_location_xx + "," + datetime.isoformat(datetime.utcnow()) + "," + str(str1))
        print("Identifiers: " + identifiers)
        dataForSending = ("\"" + str(str1) + "\"")
        cur.execute("INSERT INTO complexsensors (id, homeid, device_reporting, device_location, time_stamp, data) VALUES (%s, %s, %s, %s, %s, %s)",(UniqueID, homeID, device_reporting_xx, device_location_x, datetime.isoformat(datetime.utcnow()), dataForSending))
        pg_conn.commit()

cur.close()
pg_conn.close()
conn.close()
