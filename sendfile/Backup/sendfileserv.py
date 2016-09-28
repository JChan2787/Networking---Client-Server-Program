# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket

def ephy():
        # Create a socket
        fileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to port 0
        fileTransferSocket.bind(('',0))
        
        fileTransferSocket.listen(1)
        # Retreive the ephemeral port number
        print "I chose ephemeral port: ", fileTransferSocket.getsockname()[1]

        return fileTransferSocket




# The port on which to listen
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		
# Accept connections forever
while True:
	
        FTSock = ephy()

        # Start listening on the socket
       # FTSock.listen(1)
       

	print "Waiting for connections..."
	
	# Accept connections
	clientSock, addr = welcomeSock.accept()
        clientSock.send(str(FTSock.getsockname()[1]))

        newCSock,newAddr=FTSock.accept()
        print "Accepted connection from ephy: ", newAddr
	print "\n"
      #  FTSock.listen(1)
	
	print "Accepted connection from client: ", addr
	print "\n"
	
	# The buffer to all data received from the
	# the client.
	fileData = ""
	
	# The temporary buffer to store the received
	# data.
	recvBuff = ""
	
	# The size of the incoming file
	fileSize = 0	
	
	# The buffer containing the file size
	fileSizeBuff = ""
	
	# Receive the first 10 bytes indicating the
	# size of the file
# for fileSizeBuff, it was recvAll(FTSock,10)
	fileSizeBuff = recvAll(newCSock, 10)
		
	# Get the file size
	fileSize = int(fileSizeBuff)
	
	print "The file size is ", fileSize
	
	# Get the file data
	fileData = recvAll(newCSock, fileSize)

	print "The file data is: "
	print fileData
	#close the new stuff
	newCSock.close()
	# Close our side
	clientSock.close()
	
