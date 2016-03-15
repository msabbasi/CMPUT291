from dateutil.parser import *

class App:
	
	choices = {1: 'Vehicle Registration', 2: 'Auto Transaction Registration', 3: 'Driver Licence Registration', 4: 'Violation Record Entry', 5: 'Search Engine'}

	def __init__(self, mode, communicator):
		self.appMode = mode
		self.comm = communicator

	def run(self):
		print("Enter 'm' to go back to main menu.")
		print("Enter 'q' to quit from the system.")
		print("Enter 'c' to continue to ", self.choices[self.appMode])
		
		while(True):
			inpt = input("-->")
			if inpt == 'q':
				print("Exitting...")
				return 0
			elif inpt == 'm':
				return 1
			elif inpt == 'c':
				
				if self.appMode == 1:
					self.vehicleReg()
				elif self.appMode == 2:
					self.autoTransaction()
					return 2
				elif self.appMode == 3:
					self.driverLicenceReg()
					return 3
				elif self.appMode == 4:
					self.violationRec()
					return 4
				elif self.appMode == 5:
					self.searchEngine()
					return 5
			else:
				print("You entered an invalid input. Please try again!")
		

	def checkPersonReg(self, sin):
		curs = self.comm.connection.cursor()
		check = "SELECT * FROM people p WHERE p.sin = '" + sin + "'"
		curs.execute(check)
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

		people = {}
		people['sin'] = sin
		people['name'] = input("Name: ")
		gender = input("Gender(f/m): ")
		while(True):
			if (gender == 'f' or gender == 'm'):
				people['gender'] = gender
				break
			else:
				gender = input("Invalid entry. Please try again.\nGender(f/m): ")
		birthday = input("Birthday (dd-mm-yyyy): ")
		people['birthday'] = parse(birthday, dayfirst=True)
		people['height'] = float(input("Height (cm): "))
		people['weight'] = float(input("Weight (kg): "))
		people['eyecolor'] = input("Eye colour: ")
		people['haircolor'] = input("Hair colour: ")
		people['addr'] = input("Address: ")
		
		self.comm.insert(people, 'people')
		print("SIN#" + sin + " successfully registered.")

	def CheckSeller(self, seller_id, vehicle_id):
		curs = self.comm.connection.cursor()
		check = "SELECT * FROM owner o WHERE vehicle_id = '" + vehicle_id+" owner_id = '" + seller_id+" is_primary_owner = y'"
		curs.execute(check)
		row = curs.fetchall()
		curs.close()
		if (len(row)) == 0):
			return False
		else:
			return True
 
	def checkPersonReg(self, sin):
		curs = self.comm.connection.cursor()
		check = "SELECT * FROM people p WHERE p.sin = '" + sin + "'"
		curs.execute(check)
		row = curs.fetchall()
		curs.close()
		if (len(row) == 0):
			return False
		else:
			return True
	
	def autoTransaction(self):
		auto_sale = {}

		seller_id = input("SIN of the seller: ")
		while( len(seller_id) > 15 or seller_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			seller_id = input("SIN of the seller: ")
		if not self.checkPersonReg(seller_id):
			print("Person with the SIN entered not in system. Please register person:")
			self.regPerson(seller_id)
		auto_sale['seller_id'] = seller_id

		buyer_id = input("SIN of the buyer: ")
		while( len(buyer_id) > 15 or buyer_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			buyer_id = input("SIN of the buyer: ")
		if not self.checkPersonReg(buyer_id):
			print("Person with the SIN entered not in system. Please register person:")
			self.regPerson(buyer_id)
		auto_sale['buyer_id'] = buyer_id

		checkVReg = input("Is the vehicle registered? (y/n)  ")
		if (checkVReg == 'n'):
			vehicle_id = vehicleReg()
		else:
			vehicle_id = input("Vehicle serial #: ")
			while( len(vehicle_id) > 15 or vehicle_id == "" ):
				print("The serial number that you entered is invalid. Please try again.")
				vehicle_id = input("Vehicle serial #: ")
		auto_sale['vehicle_id'] = vehicle_id
		#TODO: Check if vehicle exists

		#TODO: Check if seller is primary owner
		if not self.CheckSeller(seller_id, vehicle_id): #Need to check primary owner. I added owner dict in vehicle registration.
			print("The person who tries to sell the vechicle is not primary owner")
			print("Please, try auto transaction with the primary owner of the vehicle")
			#del auto_sale['seller_id'] #I added these codes but I'm not sure about them.  
			#del auto_sale['buyer_id']
			#del auto_sale['vehicle_id']
			#autoTransaction()

		saleDate = input("Date of the transaction (dd-mm-yyyy): ")
		auto_sale['s_date'] = parse(saleDate, dayfirst=True) 

		auto_sale['price'] = input("Price of the vehicle sold: ")

		auto_sale['transaction_id'] = self.comm.getNewID('auto_sale', 'transaction_id')

		self.comm.insert(auto_sale, 'auto_sale')

		#TODO: Remove prev ownership

		print("Auto transaction #" + auto_sale['transaction_id'] + " successfully registered.")

		
	def driverLicenceReg(self):
		driver_licence = {}
		licence_no = input("Please enter Licence Number:")
		while( len(licence_no)>15 or license_no == ""): #If licence no has more than 15 character and does not entered anything
			print("The licence number that you entered is invalid. Please try again.")
			licence_no = input("Please enter Licence Number:")
		diver_licence['licence_no'] = licence_no
		sin = input("Please enter Social Insurance Number:")
		while( len(sin) > 15 or sin == "" ):
			print("The Social Insurance Number that you entered is invalid. Please try again.")
			sin = input("Please enter Social Insurance Number:")
		if not self.checkPersonReg(sin):
			regPerson(sin)
		driver_licence['sin'] = sin
		licence_class = input("Please enter Licence Class:")
		while ( len(licence_class)>10 or licence_no == ""):
			print ("The Licence Class that you entered is invalid. Please try again.")
			licence_class = input("Please enter Licence Class:")
		driver_licence['class'] = licence_class 
		photo_name = input("Please insert photo for licence (Optional) :")
		issuing_date = ("Please enter issuing date of the licence in MM-DD-YYYY format:")
		while ( is_date_valid(issuing_date) == False): #I need to check if it is in MM-DD-YYYY format
			print ("Issuing Date that you entered is invalid. Please try again.")
			issuing_date = ("Please enter issuing date of the licence in MM-DD-YYYY format:")
		driver_licence['issuing_date'] = issuing_date
		expiring_date = ("Please enter expiring date of the licence in MM-DD-YYYY format:")
		while ( is_date_valid(expiring_date) == False ): #I need to check if it is in MM-DD-YYYY format
			print ("Expiring Date that you entered is invalid. Please try again.")
			expiring_date = ("Please enter expiring date of the licence in MM-DD-YYYY format:")
		driver_licence['expiring_date'] = expiring_date
		print("Wait, we are processing...")
		try: 
			if (photo_name == ""):
				photo = None
			else:
				f_photo = open(photo_name, 'rb')
				photo = f_photo.read()
				driver_licence['photo'] = photo
			
			self.comm.insert(driver_licence, 'driver_licence')
			print("You registered the new driver licence!")
		except cx_Oracle.DatabaseError as exc:
			error=exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)
		

	# get info for new vehicle registration 
	def vehicleReg(self):
		vehicle = {}
		owner = {}
		# create new serial number and store in vehicle dict
		serial_no =  self.comm.getNewID('vehicle', 'serial_no')
		vehicle['serial_no'] = serial_no
		
		owner['vehicle_id'] = serial_no
		owner_id = input("Please enter the persons sin number:")
		while( len(owner_id) > 15 or owner_id == ""): # if sin is invalid
			print("The sin is invalid. Please try again.")
			owner_id = input("Please enter the persons sin number:")
		# need to check if person is in database 
		if (checkPersonReg(owner_id) == True):
			# if returns true we are ok 
			pass
		# else need to add them to database first 
		else:
			regPerson(owner_id)
		# store their sin in our owner dict 
		owner['owner_id'] = owner_id
		
		# deal with primary and secondary owners 
		# this should almost be a function on its own 
		# since if there is multiple owners need to call again to deal with this
		# but not certain
		prim_own = input("Are they a primary owner('y' or 'n'):")
		while( prim_own != 'y' or prim_own != 'n'):
			print("Invalid input. Please try again.")
			prim_own = input("Are they a primary owner('y' or 'n'):")
		owner['is_primary_owner'] = prim_own
		
		# get vehicle make 
		maker = input("Please enter the make of the vehicle:")
		while( len(maker) > 20 or maker == ""): #if maker is invalid
			print("The make that you have entered is invalid. Please try again.")
			maker = input("Please enter the make of the vehicle:")
		vehicle['maker'] = maker
		# get vehicle model
		model = input("Please enter the model of the vehicle:")
		while( len(model) > 20 or model == ""): #if model is invalid
			print("The model that you have entered is invalid. Please try again.")
			model = input("Please enter the model of the vehicle:")
		vehicle['model'] = model
		# get vehicle year
		year = int(input("Please enter the year of the vehicle:"))
		while( year > 9999 or year < 1): #if year is not between 1-4 digits 
			print("The year that you have entered is invalid. Please try again.")
			year = int(input("Please enter the year of the vehicle:"))
		vehicle['year'] = year
		# get vehicle color 
		color = input("Please enter the color of the vehicle:")
		while( len(color) > 10 or color == ""): # if color is invalid
			print("The color that you have entered is invalid. Please try again.")
			color = input("Please enter the color of the vehicle:")
		vehicle['color'] = color
		# get vehicle type_id
		# should we have function to look and find the type_id?
		type_id = int(input("Please enter the type_id:"))
		while( type(type_id) != int): # type_id not an integer
			print("The type_id is invalid. Please try again.")
			type_id = int(input("Please enter the type_id:"))
		vehicle['type_id'] = type_id
		
		# finally add the vehicle and owner to database
		self.comm.insert(vehicle, 'vehicle')
		self.comm.insert(owner, 'owner')
	
	def violationRec(self):
		
		#TODO: Better error handling
		#TODO: Optional fields?
		#TODO: Check foreign fields?

		ticket = {}

		ticket['ticket_no'] = self.comm.getNewID('ticket', 'ticket_no')

		temp = input("SIN of the violator: ")
		while( len(temp) > 15 or temp == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			temp = input("SIN of the violator: ")
		ticket['violator_no'] = temp

		#TODO: Check if person exists

		temp = input("Serial # of the vehicle involved: ")
		while( len(temp) > 15 or temp == "" ):
			print("The serial # that you entered is invalid. Please try again.")
			temp = input("Serial # of the vehicle involved: ")
		ticket['vehicle_id'] = temp

		temp = input("SIN of the officer: ")
		while( len(temp) > 15 or temp == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			temp = input("SIN of the officer: ")
		ticket['office_no'] = temp

		temp = input("Violation type: ")
		while( len(temp) > 10 or temp == "" ):
			print("Your entry is invalid. Please try again.")
			temp = input("Violation type: ")
		ticket['vtype'] = temp

		temp = input("Date of the violation (dd-mm-yyyy): ")
		ticket['vdate'] = parse(temp, dayfirst=True)

		temp = input("Place of violation: ")
		while( len(temp) > 20 or temp == "" ):
			print("Your entry is invalid. Please try again.")
			temp = input("Place of violation: ")		
		ticket['place'] = temp

		temp = input("Description: ")
		while( len(temp) > 1024 or temp == "" ):
			print("Your entry is invalid. Please try again.")
			temp = input("Description: ")	
		ticket['descriptions'] = temp

		self.comm.insert(ticket, 'ticket')

	def searchEngine(self):
		while(True):
			print("Select an option:")
			print("1. Search driver information by name")
			print("2. Search driver information by licence number")
			print("3. Search violation records by name")
			print("4. Search violation records by SIN")
			print("5. Search vehicle history by serial number")
			print("6. Return to main menu")
			choice = int(input("-->"))

			while (choice > 6 or choice < 1):
				choice = int(input("Choice not valid. Please choose a number between 1-5: "))

			if choice == 1:
				print("Driver Information")
				term = input("Enter name or leave blank to change choice: ")
			elif choice == 2:
				print("Driver Information")
				term = input("Enter licence number or leave blank to change choice: ")
			elif choice == 3:
				print("Violation Records")
				term = input("Enter name or leave blank to change choice: ")
			elif choice == 4:
				print("Violation Records")
				term = input("Enter SIN or leave blank to change choice: ")
			elif choice == 5:
				print("Vehicle History")
				term = input("Enter serial number or leave blank to change choice: ")
			else:
				break

			self.comm.search(choice, term)

