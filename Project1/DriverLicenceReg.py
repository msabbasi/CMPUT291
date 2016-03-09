def is_date_valid(date):
	correctDate = None
	try:
		this_date = datetime.strptime(date, '%m-%d-%Y')
		correctDate = True
	except ValueError:
		correctDate = False
	return correctDate
		
def DriverLicenceReg():
	print("Enter 'menu' to go back to main menu.")
	print("Enter 'quit' to quit from the system.")
	print("Enter 'insert' to register new driver licence.")
	while(True):
		Input=input("-->")
		if( Input == "quit"):
			print("Exitting...")
			break
			#sys.exit()
		if( Input == "menu"):
			MainMenu()
		if( Input == "insert"):
			licence_no = input("Please enter Licence Number:")
			while( len(licence_no)>15 or license_no == ""): #If licence no has more than 15 character and does not entered anything
				print("The licence number that you entered is invalid. Please try again.")
				licence_no = input("Please enter Licence Number:")
			sin = input("Please enter Social Insurance Number:")
                        while( len(sin) > 15 or sin == "" ):
                                print("The Social Insurance Number that you entered is invalid. Please try again.")
                                sin = input("Please enter Social Insurance Number:")
			licence_class = input("Please enter Licence Class:")
			while ( len(licence_class)>10) or licence_no = ""):
				print ("The Licence Class that you entered is invalid. Please try again.")
				licence_class = input("Please enter Licence Class:")
			photo_name = input("Please insert photo for licence (Optional) :")
			issuing_date = ("Please enter issuing date of the licence in MM-DD-YYYY format:")
			while ( is_date_valid(issuing_date) == False): #I need to check if it is in MM-DD-YYYY format
				print ("Issuing Date that you entered is invalid. Please try again.")
				issuing_date = ("Please enter issuing date of the licence in MM-DD-YYYY format:")
                        expiring_date = ("Please enter expiring date of the licence in MM-DD-YYYY format:")
			while ( is_date_valid(expiring_date) == False ): #I need to check if it is in MM-DD-YYYY format
                                print ("Expiring Date that you entered is invalid. Please try again.")
                                expiring_date = ("Please enter expiring date of the licence in MM-DD-YYYY format:")
			print("Wait, we are processing...")
			check = "SELECT * FROM people p WHERE p.sin = sin"
			curs.execute(check,{ 'p.sin' : sin})
			row = curs.fetchall()
			if (len(row) == 0):
			def DoesNotExistPerson():
				print("The person that you want to add does not exits. You need to register the person firstly/n"
				print("If you want to register a new licence enter 'new'./n Otherwise if you want to go back main menu enter 'main")
				NewInput = input("-->")
				if ( NewInput == "menu"):
					MainMenu()
				elif ( NewInput == "new"):
					DriverLicenceReg()
				else:
					print ("Invalid Entry")
					DoesNotExistPerson()
			try: 
				if (photo_name = ""):
					photo = None
				else:
					f_photo = open(photo_name, 'rb')
					photo = f_photo.read()
					curs.setinputsizes(photo=cx_Oracle.BLOB)
				insert = """ insert into drive_licence(licence_no, sin, class, photo, issuing_date, expiring_date) values (:licence_no, :sin, :class, :photo, to_date(:issuing_date, 'MM-DD-YYYY'), to_date(:expiring_date, 'MM-DD-YYYY')"""
				curs.execute(insert, {'licence_no': licence_no, 'sin': sin, 'class': licence_class, 'photo': photo, 'issuing_date':issuing_date, 'expiring_date':expiring_date})
				connection.commit()  	
				print("You registered the new driver licence!")
				print("You can choose a new option!")
				DriverLicenceReg()
				except cx_Oracle.DatabaseError as exc:
					error=exc.args
					print( sys.stderr, "Oracle code:", error.code)
					print( sys.stderr, "Oracle message:", error.message)
					print("You can choose a new option!")
					DriverLicenceReg()
		else:
			print("You entered an invalid input. Please try again!")
			Input = input("-->")	
