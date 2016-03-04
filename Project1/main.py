import sys
from communication import Comm
#import cx_Oracle

if len(sys.argv) < 2:
    mode = 0 
else:
    mode = 1

communication = Comm(mode)
communication.authenticate()

while():
	choice = int(input("""Please select the number corresponding to your choice: \n
					1 - New Vehicle Registration \n
					2 - Auto Transaction \n
					3 - Driver Licence Registration \n
					4 - Violation Record \n
					5 - Search Engine \n
					6 - Quit \n
					Type a number: """ ))
	while (choice > 6 or choice < 1):
		choice = int(input("Choice not valid. Please try again: "))

	

communication.teardown()
