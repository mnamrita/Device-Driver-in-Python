#Importing all the modules required for TCP/IP and other functions
import numpy as np 
import sys
#module for TCP/IP 
import socket
#module for making the program wait
import time
#Setting all the flags as 0 
open_connection_flag=0
Initialize_flag=0
#Creating lists of valid items
list_of_valid_operations=['Pick','Place','Transfer']
list_of_valid_parameterNames=['Source Location','Destination Location']

#Function for OpenConnection()
def OpenConnection(IPAddress):
	global open_connection_flag
	#Checking if the connection is already open 
	if open_connection_flag==0:
		try:
			socket.inet_aton(IPAddress) #Checking if the IP Address is legal or not
			
			# Create a TCP/IP socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#IP Address of the Robot and the port(1000)
			robot_address = (IPAddress,1000) 
			#Making  the connection
			sock.connect(robot_address)
			#Setting a Flag to 1 to note that the socket connection is made
			open_connection_flag=1
			#Return Empty String if no error
			ret_str=""
			return ret_str
		except socket.error as err:
			err=str(err)
			ret_str="Socket Connection  failed with error "+err
			#Return error as string
			return ret_str 
	else:
		#If connection is Open Already, return error statement
		ret_str="Connection is Already Open.Press 'Abort' if you wish to start afresh."
		return ret_str

#Function for Initialize()
def Initialize():
	#Global Variables are in use to reflect changes across all functions
	global open_connection_flag
	global Initialize_flag
	#Check if Connection is Open and initialize has not been pressed(Checking Order of Commands)
	if open_connection_flag==1 and Initialize_flag==0:
		command="home"
		message=command+"%"
		#Sending the message
		sock.sendall(message)
		#Receiving data from Mockrobot's onboard Software(processID)
		processID=sock.recv(1024)
		#checking if the processID is negative
		if processID<0:
			ret_str="Another Process is in progress. Please wait. Try again Later"
			return ret_str
		else:
			# wait for about 2 minutes(120 seconds) for the robot to complete its homing process 	
			time.sleep(120)
			#Check Status
			command="status"
			processID_string=str(processID)
			message=command+"%"+processID_string
			sock.sendall(message)
			#Get Status
			processStatus=sock.recv(1024)
			processStatus=str(processStatus)
			if processStatus=="Finished Successfully":
				Initialize_flag=1 #Set the Initialize Flag to 1
				ret_str=""
				return ret_str
			elif processStatus=="Terminated with Error":
				ret_str=processStatus
				return ret_str
			else:
				ret_str="The homing process of the robot is taking longer than usual.Abort."
				return ret_str
	else:
		ret_str="Error!Please press buttons in the order instructed"
		return ret_str

#Function for ExecuteOperation()
def ExecuteOperation(operation,parameterNames,parameterValues):
	invalid_name=0
	invalid_value=0
	global list_of_valid_operations
	global list_of_valid_parameterNames
	#First check if connection is open and robot has completed homing process
	if open_connection_flag==1 and Initialize_flag==1:
		#Checking if operation is valid 
		if operation in list_of_valid_operations:
			for x in parameterNames:
				if x not in list_of_valid_parameterNames:#Checking if parameter names are valid
					invalid_name=1
					ret_str="Error!Invalid Parameter Name"
					return ret_str
			#Checking if every value in the array/list parameterValues is an integer
			invalid_value=not(all(isinstance(item, int) for item in parameterValues))
			if invalid_value==1:
				ret_str="Error! Parameter Values should be integers"
				return ret_str
			#Checking if length of parameterNames and parameterValues match
			if len(parameterNames)!=len(parameterValues):
				ret_str="Error! The number of Parameter Values and Parameter Names don't match."
				return ret_str

			if operation=="Pick":
				if parameterNames[0]!="Source Location":
					ret_str="Incorrect Parameter Name for Pick Operation"
					return ret_str
				else:
					command="pick"
					sourceLocation=str(parameterValues[0])
					message=command+"%"+sourceLocation
					#Sending the message
					sock.sendall(message)
					processID=sock.recv(1024)
					if processID<0:
						ret_str="Another Process is in progress. Please wait. Try again Later"
						return ret_str
					else:
						# wait for about 5 minutes (300 seconds) for the robot to complete its picking process 	
						time.sleep(300)
						command="status"
						processID_string=str(processID)
						message=command+"%"+processID_string
						sock.sendall(message)
						processStatus=sock.recv(1024)
						processStatus=str(processStatus)
						if processStatus=="Finished Successfully":
							
							ret_str=""
							return ret_str
						
						elif processStatus=="Terminated with Error":
							ret_str=processStatus
							return ret_str
						else:
							ret_str="The picking process of the robot is taking longer than usual.Abort"
							return ret_str

			elif operation=="Place":
				if parameterNames[0]!="Destination Location":
					ret_str="Incorrect Parameter Name for Place Operation"
					return ret_str
				else:
					command="Place"
					destinationLocation=str(parameterValues[0])
					message=command+"%"+destinationLocation
					#Sending the message
					sock.sendall(message)
					processID=sock.recv(1024)
					if processID<0:
						ret_str="Another Process is in progress. Please wait. Try again Later"
						return ret_str
					else:
						# wait for about 5 minutes(300 seconds) for the robot to complete its placing process 	
						time.sleep(300)
						command="status"
						processID_string=str(processID)
						message=command+"%"+processID_string
						sock.sendall(message)
						processStatus=sock.recv(1024)
						processStatus=str(processStatus)
						if processStatus=="Finished Successfully":
							
							ret_str=""
							return ret_str
						
						elif processStatus=="Terminated with Error":
							ret_str=processStatus
							return ret_str
						else:
							ret_str="The placing process of the robot is taking longer than usual.Abort"
							return ret_str
			else: #This is if the operation is a transfer
				if parameterNames==['Source Location','Destination Location']:# Order of parameterNames can vary
					command="pick"
					sourceLocation=str(parameterValues[0])#Dependency on order
					message=command+"%"+sourceLocation
					#Sending the message
					sock.sendall(message)
					processID=sock.recv(1024)
					if processID<0:
						ret_str="Another Process is in progress. Please wait. Try again Later"
						return ret_str
					else:
						# wait for about 5 minutes for the robot to complete its picking process 	
						time.sleep(300)
						command="status"
						processID_string=str(processID)
						message=command+"%"+processID_string
						sock.sendall(message)
						processStatus=sock.recv(1024)
						processStatus=str(processStatus)
						if processStatus=="Terminated with Error":
							ret_str=processStatus
							return ret_str
							
							
							
						
						elif processStatus=="In Progress":
							ret_str="The picking process of the robot is taking longer than usual.Abort"
							return ret_str
						#Go ahead with Place, If Pick was a success
						else:
							command="Place"
							destinationLocation=str(parameterValues[1])#Dependency on order
							message=command+"%"+destinationLocation
							#Sending the message
							sock.sendall(message)
							processID=sock.recv(1024)
							if processID<0:
								ret_str="Another Process is in progress. Please wait. Try again Later"
								return ret_str
							else:
								# wait for about 5 minutes(300 seconds) for the robot to complete its placing process 	
								time.sleep(300)
								command="status"
								processID_string=str(processID)
								message=command+"%"+processID_string
								sock.sendall(message)
								processStatus=sock.recv(1024)
								processStatus=str(processStatus)
								if processStatus=="Finished Successfully":
									
									ret_str=""
									return ret_str
								
								elif processStatus=="Terminated with Error":
									ret_str=processStatus
									return ret_str
								else:
									ret_str="The placing process of the robot is taking longer than usual.Abort"
									return ret_str

				elif parameterNames==['Destination Location','Source Location']:#Order of parameterNames interchanged
					command="pick"
					sourceLocation=str(parameterValues[1])#Dependency on order
					message=command+"%"+sourceLocation
					#Sending the message
					sock.sendall(message)
					processID=sock.recv(1024)
					if processID<0:
						ret_str="Another Process is in progress. Please wait. Try again Later"
						return ret_str
					else:
						# wait for about 5 minutes(300 seconds) for the robot to complete its picking process 	
						time.sleep(300)
						command="status"
						processID_string=str(processID)
						message=command+"%"+processID_string
						sock.sendall(message)
						processStatus=sock.recv(1024)
						processStatus=str(processStatus)
						if processStatus=="Terinated with Error":
							ret_str=processStatus
							return ret_str
							
							
							
						
						elif processStatus=="In Progress":
							ret_str="The picking process of the robot is taking longer than usual.Please press 'Abort' to abort the process and begin afresh."
							return ret_str
						#Go ahead with Place, If Pick was a success
						else:
							command="Place"
							destinationLocation=str(parameterValues[0])#Dependency on order
							message=command+"%"+destinationLocation
							#Sending the message
							sock.sendall(message)
							processID=sock.recv(1024)
							if processID<0:
								ret_str="Another Process is in progress. Please wait. Try again Later"
								return ret_str
							else:
								# wait for about 5 minutes for the robot to complete its placing process 	
								time.sleep(300)
								command="status"
								processID_string=str(processID)
								message=command+"%"+processID_string
								sock.sendall(message)
								processStatus=sock.recv(1024)
								processStatus=str(processStatus)
								if processStatus=="Finished Successfully":
									
									ret_str=""
									return ret_str
								
								elif processStatus=="Terminated with Error":
									ret_str=processStatus
									return ret_str
								else:
									ret_str="The placing process of the robot is taking longer than usual.Please press 'Abort' to abort the process and begin afresh."
									return ret_str

		else:
			ret_str="Invalid Operation"	
			return ret_str

#Function for Abort()
def Abort():
	global open_connection_flag
	#First check if connection is open(Only then can you  Abort)
	if open_connection_flag==1:
		#Close the socket, or end the connection
		sock.close()
		#Set the openconnection flag as 0, to indicate it is now closed
		open_connection_flag=0
		ret_str=""
		return ret_str

	else:
		ret_str="No communication with robot exixts. No need to Abort."
		return ret_str


		





								








