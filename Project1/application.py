

class App:
	
	choices = {1: 'Vehicle Registration', 2: 'Auto Transaction Registration', 3: 'Driver Licence Registration', 4: 'Violation Record Entry', 5: 'Search Engine'}

	def __init__(self, mode, communicator):
		self.appMode = mode
		self.comm = communicator

	def run(self):
		print("Enter 'm' to go back to main menu.")
		print("Enter 'q' to quit from the system.")
		print("Enter 'c' to continue to ", choices[self.appMode])
		
		while(True):
			inpt = input("-->")
			if inpt == 'q':
				print("Exitting...")
				return 0
			elif inpt == 'm':
				return 1
			elif inpt == 'c':
				
				if self.appMode == 1:
					vehicleReg()
				elif self.appMode == 2:
					autoTransaction()
					return 2
				elif self.appMode == 3:
					driverLicenceReg()
					return 3
				elif self.appMode == 4:
					regPerson()
					return 4
			else:
				print("You entered an invalid input. Please try again!")
		

	def checkPersonReg(self, sin):
		curs = self.comm.cursor()
		check = "SELECT * FROM people p WHERE p.sin = :sin"
		curs.execute(check,{'sin' : sin})
		row = curs.fetchall()
		curs.close()
		if (len(row) == 0):
			return False
		else:
			return True

	def is_date_valid(date):
		correctDate = None
		try:
			this_date = datetime.strptime(date, '%m-%d-%Y')
			correctDate = True
		except ValueError:
			correctDate = False
		return correctDate

	def regPerson(self, sin):
		#people = {'sin': 'abcd', 'name': 'abcd', 'height': 5.20, 'weight': 5.20, 'eyecolor': 'blue', 'haircolor': 'brown', 'addr': '123 45 Ave NW, Edmonton', 'gender': '?', 'birthday': '12-03-96'}

		people = {}
		people['sin'] = sin
		people['name'] = input("Name: ")
		people['gender'] = input("Gender(f/m): ")
		people['birthday'] = input("Birthday (yy-mm-dd): ")
		people['height'] = input("Height: ")
		people['weight'] = input("Weight: ")
		people['eyecolor'] = input("Eye colour: ")
		people['haircolor'] = input("Hair colour: ")
		people['addr'] = input("Address: ")
		
		self.comm.insert(people)

	def vehicleReg(self):
		return


	def autoTransaction(self):
		auto_sale = {}

		seller_id = input("Please enter the SIN of the seller: ")
		while( len(seller_id) > 15 or seller_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			seller_id = input("Please enter the SIN of the seller: ")
		if not checkPersonReg(seller_id):
			regPerson(seller_id)
		auto_sale['seller_id'] = seller_id

		buyer_id = input("Please enter the SIN of the buyer: ")
		while( len(buyer_id) > 15 or buyer_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			buyer_id = input("Please enter the SIN of the buyer: ")
		if not checkPersonReg(buyer_id):
			regPerson(buyer_id)
		auto_sale['buyer_id'] = buyer_id

		checkVReg = input("Is the vehicle registered? (y/n)  ")
		if (checkVReg == n):
			vehicle_id = vehicleReg()
		else:
			vehicle_id = input("Please enter the vehicle serial #: ")
			while( len(vehicle_id) > 15 or vehicle_id == "" ):
				print("The serial number that you entered is invalid. Please try again.")
				vehicle_id = input("Please enter the vehicle serial #: ")
		auto_sale['vehicle_id'] = vehicle_id

		
		auto_sale['s_date'] = input("Please enter the date of the transaction (yy-mm-dd): ")

		auto_sale['price'] = input("Please enter the price of the vehicle sold: ")

		auto_sale['transaction_id'] = self.comm.getNewID('auto_sale')

		self.comm.insert(auto_sale)

		
	def driverLicenceReg():
		driverLicenceReg = {}
		licence_no = input("Please enter Licence Number:")
		while( len(licence_no)>15 or license_no == ""): #If licence no has more than 15 character and does not entered anything
			print("The licence number that you entered is invalid. Please try again.")
			licence_no = input("Please enter Licence Number:")
		diverLicenceReg['licence_no'] = licence_no
		sin = input("Please enter Social Insurance Number:")
		while( len(sin) > 15 or sin == "" ):
			print("The Social Insurance Number that you entered is invalid. Please try again.")
			sin = input("Please enter Social Insurance Number:")
		licence_class = input("Please enter Licence Class:")
		while ( len(licence_class)>10 or licence_class == ""):
			print ("The Licence Class that you entered is invalid. Please try again.")
			licence_class = input("Please enter Licence Class:")
		driverLicenceReg['class'] = licence_class 
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
#				print("If you want to register a new licence enter 'new'.\n Otherwise if you want to go back main menu enter main")
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
		

	# get info for new vehicle registration 
	def vehicleReg(): 
		serial_no = input("Please enter vehicle serial number:")
		while( len(serial_no) > 15 or serial_no == ""): #if serial_no is invalid
		print("The serial number that you have entered is invalid. Please try again.")
		serial_no = input("Please enter vehicle serial number:")		
		
		maker = input("Please enter the make of the vehicle:")
		while( len(maker) > 20 or maker == ""): #if maker is invalid
		print("The make that you have entered is invalid. Please try again.")
		maker = input("Please enter the make of the vehicle:")
		
		model = input("Please enter the model of the vehicle:")
		while( len(model) > 20 or model == ""): #if model is invalid
		print("The model that you have entered is invalid. Please try again.")
		model = input("Please enter the model of the vehicle:")
		
		year = int(input("Please enter the year of the vehicle:"))
		while( year > 9999 or year < 1): #if year is not between 1-4 digits 
		print("The year that you have entered is invalid. Please try again.")
		year = int(input("Please enter the year of the vehicle:"))
		
		color = input("Please enter the color of the vehicle:")
		while( len(color) > 10 or color == ""): # if color is invalid
		print("The color that you have entered is invalid. Please try again.")
		color = input("Please enter the color of the vehicle:")
		
		type_id = int(input("Please enter the type_id:"))
		while( type(type_id) != int): # type_id not an integer
			print("The type_id is invalid. Please try again.")
			type_id = int(input("Please enter the type_id:"))
		
		owner_id = input("Please enter the persons sin number:")
		while( len(owner_id) > 15 or owner_id == ""): # if sin is invalid
			print("The sin is invalid. Please try again.")
			owner_id = input("Please enter the persons sin number:")
		
		prim_own = input("Are they a primary owner('y' or 'n'):")
		while( prim_own != 'y' or prim_own != 'n'):
			print("Invalid input. Please try again.")
			prim_own = input("Are they a primary owner('y' or 'n'):")
			
	
