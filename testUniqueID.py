#test code to make sure we can create unique IDs

for n in range (0,8):
	f = open("/directoryTo/UniqueID.txt", 'r+')
	UniqueID = f.read()
	#print(UniqueID)
	UniqueID = int(UniqueID) + 1
	print(UniqueID)
	f.seek(0)
	f.write(str(UniqueID))
	f.truncate()
	f.close()