import sys
from communication import Comm
from application import App

if len(sys.argv) < 2:
    mode = 0 
else:
    mode = 1

# Start up an instance of the communicator
communication = Comm(mode)
communication.authenticate()

while(True):
	print()
	print("====================================================================")
	print("                               MAIN MENU                            ")
	print("====================================================================")

	# Get the user to choose an option
	try:
		choice = int(input("""Please select the number corresponding to your choice: \n1 - New Vehicle Registration \n2 - Auto Transaction \n3 - Driver Licence Registration \n4 - Violation Record \n5 - Search Engine \n6 - Quit \nType a number: """ ))
	except ValueError:
		choice = 0
	while (choice > 6 or choice < 1):
		try:
			choice = int(input("Choice not valid. Please choose a number between 1-6: "))
		except ValueError:
			choice = 0

	# Exit if exit option choosen
	if (choice == 6):
		print("Exiting...")
		break

	# Start the app supplying the choice and the communicator
	app = App(choice, communication)
	result = app.run()

	# Exit if the user choose to quit
	if result == 0:
		break
	

# Clean up
communication.teardown()
