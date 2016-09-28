# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys
import commands

#Setting global values
# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

def lls_flag():

        # Run ls command, get output, and print it
        for line in commands.getstatusoutput('ls -l'):
                print line



def put_flag(file_name, conn_sock):
        
	# Command line checks 
	#if len(sys.argv) < 2:
	#	print "USAGE python " + sys.argv[0] + " <FILE NAME>" 

	# Server address
	#serverAddr = "localhost"

	# Server port
	#serverPort = 1234

	# The name of the file
	#fileName = sys.argv[1]

	# Open the file
	fileObj = open(file_name, "r")

	# Create a TCP socket
	#connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	#connSock.connect((serverAddr, serverPort))

	# Create ephermal socket

	ephyPort = conn_sock.recv(1024)
	print ephyPort
	x = int(ephyPort)
	print x
	ephySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ephySock.connect((serverAddr, x))
	print "ephy in client->server success"
	# The number of bytes sent
	numSent = 0

	#indicator for continuing to print ftp>
	stillNotQuit =True
	# The file data
	fileData = None

	print("Inside put flag")

	# Keep sending until all is sent
	while True:

		# Open the file
		fileObj = open(file_name, "r")

		# Read 65536 bytes of data
		fileData = fileObj.read(65536)
	
		# Make sure we did not hit EOF
		if fileData:
					
			# Get the size of the data read
			# and convert it to string
		        # The ? signifies for the server that it is the end of the file name
			dataSizeStr = str(len(file_name + "?" + fileData))
		
			# Prepend 0's to the size string
			# until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
	
	
			# Prepend the size of the data to the
			# file data.
			fileData = dataSizeStr + file_name + "?" + fileData	
		
			# The number of bytes sent
			print("Setting numSent to zero")
			numSent = 0
			
			# Send the data!
			while len(fileData) > numSent:
				#numSent += connSock.send(fileData[numSent:])
				#print("Length of file data " +str(len(fileData)) + "\nNumber of bytes sent: " + str(numSent))
				temp = ephySock.send(fileData[numSent:])
				print("temp is: " + str(temp))				
				print("numSent before: " + str(numSent))
		                numSent = numSent + temp
				print("numSent after: " + str(numSent))
				
	
		# The file has been sent. We are done
		#else:
			print("File sent :^)")
			break


	print "Sent ", numSent, " bytes over ephemeral socket: ", ephySock.getsockname()[1]
	
	# Close the socket and the file
	# conn_sock.close()
	ephySock.close()
	fileObj.close()
	



def main(): 
	# Server address
	#serverAddr = "localhost"

	# Server port
	#serverPort = 1234

	# Create a TCP socket
	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	connSock.connect((serverAddr, serverPort))

        
	while True:
		answer = raw_input("FTP> ")
		
		print(answer)                 	

		if answer == "lls":
			lls_flag()
		
		if answer[:3] == "put":	
			print("put flag triggered")	
			put_flag(answer[4:], connSock)
                 
                if answer == "quit":
                         sys.exit()
                 
if __name__ == "__main__":
        main()


