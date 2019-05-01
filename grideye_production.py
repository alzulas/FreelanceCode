## Author: Leah Zulas, April 2019
## This program takes readings from the AMG88xx GridEye 8x8 sensor
## It determines if the data is a significant change from an average of the last 4 readings
## If the data is a significant change, it uses a socket from the Pi0w to the Pi3+ to send this reading
## Onlt the Pi3 has the ability to send data to the server, therefore, this code does not do that. 

import busio
import adafruit_amg88xx
import board
import time
from datetime import datetime
import socket
import matplotlib.pyplot as plt
import numpy as np 
import queue

#This method determines if the average of the last four readings is more than 3 degrees different. 
def changeCheck (data, Mavg):
    #print("New array", data)
    for i in range (0,8):
        for j in range (0,8):
            dif = Mavg[i][j] - data[i][j]
            if(abs(dif) > 3):
                print ("Number: " + str(abs(dif)) + "in element " + str(i) + " and " + str(j) + " at time stamp: " + datetime.isoformat(datetime.utcnow()))
                return(True)
    return(False)

def main():
    
    #Device information
    #homeID = "xxx"
    #device_reporting = "AMG88xx_Grid_Eye"
    #device_location = "Bedroom"
    #fileLocation = "/home/pi/UniqueIDIterator.txt"

    iterationCounter = 0;
    mAvgCreated = False
    changeOccured = False
    tmp = []
    Mavg = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    q = queue.Queue(0)
    #The data is a list of lists in a queue. It's an 8 x 8 matrix (list of lists) and the last four readings are always stored in a queue. 

    TCP_IP = 'xx.xx.xx.xx'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024

    #This makes the connection to the board and creates an object amg which is the sensor
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c_bus)
    amg = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x69)


    #str1 = ''.join(str(e) for e in amg.pixels)
    #print (type(str1))

#main loop
    while True:
        #Get data reading:
        data = amg.pixels

    #Printing for testing
        #for x in data:
        #    print(x)

        #Find out if the change is significant
        if (mAvgCreated):
            changeOccured = changeCheck(data, Mavg)
            print(changeOccured)
            if (changeOccured):
                iterationCounter = 10
            #reset average
            Mavg = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        #print("New array", data)

        #Code to begin the sensor. To gather the first 4 readings
        if (q.qsize() <= 3):
            q.put(data)
            print("<=3")
            #testing for queue
            #for elem in list(q.queue):
            #    print(elem)
        else: #This section actually does work on the queue
            print("queue size is: " + str(q.qsize()))
            #tmp isn't really important here, just allows a pop and push. 
            tmp = q.get()
            q.put(data)
            print(">3")
            #testing for the queue
            #for elem in list(q.queue):
               #print(elem)
            #Iterating through the list of lists and the queue to make an average 
            for i in range (0,8):
                for j in range (0,8):
                   for elem in list(q.queue):
                        Mavg[i][j] = elem[i][j] + Mavg[i][j]
                   Mavg[i][j] = Mavg[i][j]/4
        #print("Mavg = ", Mavg)
            #This variable just begins the checking sequence after the queue is full. 
            mAvgCreated = True
        #try every second
        if (iterationCounter > 0):
            #Get data
            str1 = ''.join(str(e) for e in amg.pixels)
            dataString = str1.encode('utf-8')
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.sendall(dataString)
            datares = s.recv(BUFFER_SIZE)
            s.close()
            iterationCounter = iterationCounter - 1

            print ("received data:", datares)
        time.sleep(1)



if __name__ == "__main__":
    main()
