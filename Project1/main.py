import sys
from communication import Comm
from application import App
#import cx_Oracle

if len(sys.argv) < 2:
    mode = 0 
else:
    mode = 1

communication = Comm(mode)
communication.authenticate()

while(True):
	choice = int(input("""Please select the number corresponding to your choice: \n1 - New Vehicle Registration \n2 - Auto Transaction \n3 - Driver Licence Registration \n4 - Violation Record \n5 - Search Engine \n6 - Quit \nType a number: """ ))
	while (choice > 6 or choice < 1):
		choice = int(input("Choice not valid. Please choose a number between 1-6: "))
	if (choice == 6):
		break

	communication.getNewID('people')
	communication.getNewID('owner')
	app = App(choice, communication)
	#result = app.run()
	#if result == 0:
	#	break
	


communication.teardown()
