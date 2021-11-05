import socket
import sys
import time
#import busio
#import digitalio
#import board
#import adafruit_mcp3xxx.mcp3008 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import datetime


def threads():
    #sends data through tcp constrantly
    while(True):
        lightval = 32#channel1.value
        tempval = 32#round(channel2.voltage*100)
        #sensor 'ON'
        if(circuitstat):
            sendTo(tempval, lightval)
        
        #Wait for 10s     
        time.sleep(10)


#def stat():
#    if(lastsample == None):
#        s.send('There is no last sample!'.encode())
#        message = 'True ' + "%" + lastsample
#        length = len(message)
#        message = 'True ' + length + "%" + lastsample

def sendTo(temp, light):
    global lastsample
    #putting message into a specific format
    message = str(light) + "#" + str(temp)
    #getting the length of the message
    length = len(message)
    #concatenating the message with the cmd,length and message
    message = "S" + str(length) + " "+ message
    #Message format: <cmd> <length> <light>#<temp>
    s.send(message.encode())
    #Note time as the new latest sample   
    lastsample = str(datetime.now().time())[0:8]
################TCP SEND SETUP###########################

#TODO Add code to setup the tcp connection with the correct IP and same port as the tcp_server on the other pi
    #Test this locally before trying to deploy via balena using test messages instead of ADC values
    #Use localmode when deploying to balena and use the advertised local address (using public IPs is possible but more complicated to configure due to the security measures BalenaOS imposes by default.  These are a good thing for real world deployment but over complicate the prac for the immediate purposes

S_IP = '192.168.43.252' #enter the server's local ip address
S_PORT = 5003  #enter the server's port number
buffer = 25 # the buffer size for receiving data from the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
#Active = 'Client is active'  #client status
circuitstat = True
lastsample = None
channel1 = None
channel2 = None



print('Working')            

# connect to the server on local computer
print('Trying to connect')   
try:
    s.connect((S_IP, S_PORT))
    print('Connected')  
except:
    print('Connection failed!') 

# receive data from the server and decoding to get the string.
print (s.recv(buffer).decode())

    #preparing the light and temperature sensor channels and buttons
    
    #spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    #cs = digitalio.DigitalInOut(board.D5)
    #mcp = MCP.MCP3008(spi, cs)


    #chan_temp = AnalogIn(mcp, MCP.P1)
    #chan_LDR = AnalogIn(mcp, MCP.P2)


    #notifies server that client is still active
    #s.send(Active.encode())

    #threading code is below
td  = threading.Thread(target = threads)
td.daemon = True
td.start()

##################ADC Setup##############################

#TODO using the adafruit circuit python SPI and MCP libraries setup the ADC interface
#Google will supply easy to follow instructions 








#########################################################

print("Sensor Node it awake\n")     #Print statements to see what's happening in balena logs
#f.write("Sensor Node it awake\n")   #Write to file statements to see what's happening if you ssh into the device and open the file locally using nano
#f.flush()
s.send(b'Sensor Node it awake\n')   #send to transmit an obvious message to show up in the balena logs of the server pi

while(True):
   



    #TODO add code to read the ADC values and print them, write them, and send them

    #Input = input('Enter a command: ') #asks client for a command
    serverIn = s.recv(buffer)
    serverIn = serverIn.decode('utf-8')

    if(serverIn == 'Exit'): #Exits the server program if the user inputs “Exit” and sends Input to the server
	    s.send('Client has Terminated the session'.encode()) #notifies server that client is no longer active
	    break

    elif(serverIn == 'On'): #turns on the sensors for server
        s.send('Sensors On'.encode())
        circuitstat = True
        pass
	        #circuit code on

    elif(serverIn == 'Off'): #turns off sensors for server
        s.send('Sensors Off'.encode())
        circuitstat = False
        pass
	        #circuit code off


    elif(serverIn == 'Status'): #checks if sensors are on or off
            
        if(circuitstat == True):
            s.send('On'.encode())
            s.send(lastsample.encode())
        else:
            s.send('Off'.encode())
                
    
    # close the connection
s.close()
print('Finished')   



    
time.sleep(5)


