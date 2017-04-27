'''
Example RIO Datalogging Application

To Run:
From the terminal, call the .py file with the first argument being the gclib connection string.

Example:
python rio_datalog_simple.py "192.168.10.10 --direct"


'''
import gclib
import sys
import datetime
#Create a log file with the current date and time.
filename = 'temperature_read_{:%Y-%m-%d_%H_%M}.csv'.format(datetime.datetime.now())
f=open(filename,"w")        #Open the new log file to save
g=gclib.py()                #Create the gclib object
print ("RIO-47122, Raspberry Pi Temperature Datalogger")
print ("gclib version: ",g.GVersion() )#Print the gclib version
try:
  g.GOpen(sys.argv[1])      #Use command line argument for connection string to PLC
  print (g.GInfo())         #Print the PLC info
  g.GCommand("AQ1,3")       #set analog input 1 to 0-5V
  try:
    while True:             #loop until ^C is sent from keyboard
        readTemp = (float(g.GCommand("MG @AN[1]")) * 1000.0)/10.15 # mV/deg C - type K
        readTemp = readTemp * 1.8 + 32# Convert to Degrees
        print(readTemp)     #Print to the screen
                            #Write a data row
        f.write(str(datetime.datetime.now())+","+str(round(readTemp,2))+"\n")
        f.flush()           #Tell Python to periodically save data to the disk
        g.GSleep(60000)     #Update every minute
  except KeyboardInterrupt:
    pass
except Exception as e:
  print ("Error: ", str(e)) #print the error description
finally:
  print ("\nDone, closing connection")
  g.GClose()                #Close gclib connection
  f.close()                 #Close file connection and write to disk