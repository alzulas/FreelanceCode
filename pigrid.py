#This was mostly a lot of testing. 
#This wasn't used in production




#import busio
#import adafruit_amg88xx
#import board
import time
import socket
import matplotlib.pyplot as plt
import numpy as np 
import random
import queue

#queues
#from dataclasses import dataclass, field
#from typing import Any

mAvgCreated = False
randArray = []
tmp = []
Mavg = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
q = queue.Queue(0)

#i2c_bus = busio.I2C(board.SCL, board.SDA)
#amg = adafruit_amg88xx.AMG88XX(i2c_bus)
#amg = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x69)
#plt.ion()
#plt.show(block=False)
#fig = plt.figure()
#str1 = ''.join(str(e) for e in amg.pixels)
#print (type(str1))
while True:
    #data = amg.pixels
	#create a bunch of random numbers
	randArray = np.random.randint(0,50, size=(8,8))
	#print the array, just so I know you're not broken
	#for x in randArray:
	#	print(x)

	if (mAvgCreated):
		print("New array", randArray)
		for i in range (0,8):
			for j in range (0,8):
				dif = Mavg[i][j] - randArray[i][j]
				if(abs(dif) > 4):
					print (abs(dif))
		Mavg = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

	if (q.qsize() <= 3):
		q.put(randArray)
		print("<=3")
		#for elem in list(q.queue):
		#	print(elem)
	else:
		tmp = q.get()
		q.put(randArray)
		print(">3")
		#for elem in list(q.queue):
		#	print(elem)
		for i in range (0,8):
			for j in range (0,8):
				for elem in list(q.queue):
					Mavg[i][j] = elem[i][j] + Mavg[i][j]
				Mavg[i][j] = Mavg[i][j]/4
		print("Mavg = ", Mavg)
		mAvgCreated = True
	
	print("Pausing...")
	time.sleep(10)





#working on images
 #This is my attempt to clear.	
	#if (first == False):
	#	plt.clf()
	#first = False
	#basical visualization
	#ax = fig.add_subplot(111)
	#h = ax.imshow(randArray, cmap='hot', interpolation='nearest')
	#h.set()
	#plt.draw()
	#lt.show()
	#fig.canvas.draw()
	#fig.canvas.flush_events()
    #plt.canvas.draw()
#    plt.display.update