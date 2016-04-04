import sys

if len(sys.argv) < 2:
    print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or index")
    sys.exit()
else:
    mode = sys.argv[1]
    if mode != 'btree' and mode != 'hash' and mode != 'index':
        print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or index")
        sys.exit()


while(True):
	print()
	print("====================================================================")
	print("                               MAIN MENU                            ")
	print("====================================================================")

	# Get the user to choose an option
	try:
		choice = int(input("""Please select the number corresponding to your choice: \n1 - Create and populate a database \n2 - Retrieve records with a given key \n3 - Retrieve records with a given data \n4 - Retrieve records with a given range of key values \n5 - Destroy the database \n6 - Quit \nType a number: """ ))
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


	print(mode)
	# Start the app supplying the choice and the communicator
	#app = App(choice, communication)
	#result = app.run()

	# Exit if the user choose to quit
	#if result == 0:
	#	break
	

# Clean up

