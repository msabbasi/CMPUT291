from dateutil.parser import *
from datetime import *
import cx_Oracle
import sys 
import os

class App:
	
	choices = {1: 'Vehicle Registration', 2: 'Auto Transaction Registration', 3: 'Driver Licence Registration', 4: 'Violation Record Entry', 5: 'Search Engine'}
	searchChoices = {1: "Driver Information by Name", 2: "Driver Information by Licence Number", 3: "Violation Records by Licence Number", 4: "Violation Records by SIN", 5: "Vehicle History by Serial Number"}

	def __init__(self, mode, communicator):
		self.appMode = mode
		self.comm = communicator

	def run(self):
		print()
		print("====================================================================")
		print("                      ", self.choices[self.appMode])
		print("====================================================================")
		
		while(True):
			print("\nEnter 'm' to go back to main menu.")
			print("Enter 'q' to quit from the system.")
			print("Enter 'c' to continue to ", self.choices[self.appMode])
			inpt = input("-->")
			if inpt == 'q':
				print("Exiting...")
				return 0
			elif inpt == 'm':
				return 1
			elif inpt == 'c':
				print()

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

	def is_date_valid(self, date):
		correctDate = None
		try:
			this_date = datetime.strptime(date, '%m-%d-%Y')
			correctDate = True
		except ValueError:
			correctDate = False
		return correctDate

	def regPerson(self, sin):

		print("\nPerson with the SIN entered not in system. Please register person:")

		people = {}
		people['sin'] = sin
		temp = input("Name: ").strip()
		while( temp == ""):
			print("Invalid input. Please try again.")
			temp = input("Name: ").strip()
		people['name'] = temp
		gender = input("Gender(f/m): ").strip()
		while(True):
			if (gender == 'f' or gender == 'm'):
				people['gender'] = gender
				break
			else:
				gender = input("Invalid entry. Please try again.\nGender(f/m): ").strip()
		birthday = input("Birthday (mm-dd-yyyy): ").strip()
		while (self.is_date_valid(birthday) == False): 
			print ("The date entered is invalid. Please try again.")
			birthday = input("Birthday (mm-dd-yyyy): ")
		people['birthday'] = parse(birthday, dayfirst=False)
		people['height'] = None
		while (people['height'] == None or people['height'] == ""):
			try:
				people['height'] = float(input("Height (cm): ").strip())
			except ValueError:
				print("Invalid input. Please enter a number.")
				people['height'] = None
		people['weight'] = None
		while (people['weight'] == None or people['weight'] == ""):
			try:
				people['weight'] = float(input("Weight (kg): "))
			except ValueError:
				print("Invalid input. Please enter a number.")
		temp = input("Eye colour: ").strip()
		while( temp == ""):
			print("Invalid input. Please try again.")
			temp = input("Eye colour: ").strip()
		people['eyecolor'] = temp
		temp = input("Hair colour: ").strip()
		while( temp == ""):
			print("Invalid input. Please try again.")
			temp = input("Hair colour: ").strip()
		people['haircolor'] = temp
		temp = input("Address: ").strip()
		while( temp == ""):
			print("Invalid input. Please try again.")
			temp = input("Address: ").strip()
		people['addr'] = temp		
		self.comm.insert(people, 'people')
		self.comm.connection.commit()
		print("SIN#" + sin + " successfully registered.\n")

	def CheckPrimaryOwner(self, seller_id, vehicle_id):
		curs = self.comm.connection.cursor()
		check = "SELECT * FROM owner o WHERE vehicle_id = '" + vehicle_id+"' AND owner_id = '" + seller_id+"' AND is_primary_owner = 'y'"
		curs.execute(check)
		row = curs.fetchall()
		curs.close()
		if (len(row) == 0):
			return False
		else:
			return True
	

	def CheckIfPersonHasLicence(self, sin):
		curs = self.comm.connection.cursor()
		check = "SELECT * FROM drive_licence dl WHERE dl.sin = '" + sin + "'"
		curs.execute(check)
		row = curs.fetchall()
		curs.close()
		if (len(row) == 0):
			return True
		else:
			return False 
	
	# check if vehicle is in system 
	def checkVehicleReg(self, serial_no):
		# create cursor
		curs = self.comm.connection.cursor()
		# create sql statement
		check = "SELECT * FROM vehicle v WHERE v.serial_no = '" + serial_no + "'"
		# execute 
		curs.execute(check)
		row = curs.fetchall()
		curs.close()
		# check results 
		if (len(row) == 0):
			return False
		else:
			return True
			
	# function to deal with primary/secondary owners 
	def addOwner(self, owner, mode):
		# get owner_id
		owner_id = input("Please enter the owner's sin number: ")
		while( len(owner_id) > 15 or owner_id == ""): # if sin is invalid
			print("The sin is invalid. Please try again.")
			owner_id = input("Please enter the owner's sin number: ")
		# need to check if person is in database 
		if (self.checkPersonReg(owner_id) == True):
			# if returns true we are ok 
			pass
		# else need to add them to database first 
		else:
			self.regPerson(owner_id)
		# add their sin to our dict
		owner['owner_id'] = owner_id
		if (mode == 0):
			# is primary owner?
			prim_own = input("Are they a primary owner('y' or 'n'): ")
			while( prim_own != 'y' and prim_own != 'n'):
				print("Invalid input. Please try again.")
				prim_own = input("Are they a primary owner('y' or 'n'): ")
			# add response to our dict	
			owner['is_primary_owner'] = prim_own	
		# return owner dictionary
		return owner
	
	def removePrevOwners(self, serial_no):
		curs = self.comm.connection.cursor()
		check = "DELETE FROM owner o WHERE o.vehicle_id = '" + serial_no + "'"
		curs.execute(check)
		self.comm.connection.commit()
		curs.close()

	def autoTransaction(self):
		auto_sale = {}

		print("Please provide the following information.\n")

		vehicle_id = input("Vehicle serial #: ")
		while( len(vehicle_id) > 15 or vehicle_id == "" ):
			print("The serial number that you entered is invalid. Please try again.")
			vehicle_id = input("Vehicle serial #: ")
		auto_sale['vehicle_id'] = vehicle_id
		if not self.checkVehicleReg(vehicle_id):
			print("This vehicle is not registered. Please register the vehicle first.")
			return

		seller_id = input("SIN of the seller: ")
		while( len(seller_id) > 15 or seller_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			seller_id = input("SIN of the seller: ")
		if not self.checkPersonReg(seller_id):
			self.regPerson(seller_id)
		auto_sale['seller_id'] = seller_id

		if not self.CheckPrimaryOwner(seller_id, vehicle_id): 
			print("\nThe seller is not the primary owner.")
			print("Please try auto transaction with the primary owner of the vehicle.")
			return

		buyer_id = input("SIN of the buyer: ")
		while( len(buyer_id) > 15 or buyer_id == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			buyer_id = input("SIN of the buyer: ")
		if not self.checkPersonReg(buyer_id):
			self.regPerson(buyer_id)
		auto_sale['buyer_id'] = buyer_id

		
		saleDate = input("Date of the transaction (mm-dd-yyyy): ")
		while (self.is_date_valid(saleDate) == False): 
			print ("The date entered is invalid. Please try again.")
			saleDate = input("Date of the transaction (mm-dd-yyyy): ")
		auto_sale['s_date'] = parse(saleDate, dayfirst=False) 

		auto_sale['price'] = None
		while (auto_sale['price'] == None):
			try:
				auto_sale['price'] = float(input("Price of the vehicle sold: "))
			except ValueError:
				print("Input not valid. Please enter a numeric number.")
				auto_sale['price'] = None

		auto_sale['transaction_id'] = self.comm.getNewID('auto_sale', 'transaction_id')

		self.comm.insert(auto_sale, 'auto_sale')

		self.removePrevOwners(vehicle_id)


		owner = {}
		owner['vehicle_id'] = vehicle_id
		owner['owner_id'] = buyer_id
		owner['is_primary_owner'] = 'y'
				
		self.comm.insert(owner, 'owner')

		while(True):
			another = input('Press y to add another owner or press any other key to return to the main menu. ')
			
			if (another != 'y'):
				break

			owner = self.addOwner(owner, 0)
			try:
				self.comm.insert(owner, 'owner')
				print("Owner added.")
			except cx_Oracle.DatabaseError as exc:
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				#print( sys.stderr, "Oracle message:", error.message)
				print("This person is already an owner of this vehicle.")

		print("Auto transaction #" + auto_sale['transaction_id'] + " successfully registered.")

		
	def driverLicenceReg(self):
		#TODO: Restrictions (Conditions)

		driver_licence = {}

		driver_licence['licence_no'] = self.comm.getNewID('drive_licence', 'licence_no')
		
		sin = input("Please enter Social Insurance Number:") #Ask sin
		while( len(sin) > 15 or sin == "" ): #Check the sin is valid or not
			print("The Social Insurance Number that you entered is invalid. Please try again.")
			sin = input("Please enter Social Insurance Number:")
		if not self.checkPersonReg(sin): #If the person is not registered, register the person first of all
			self.regPerson(sin)
		if not self.CheckIfPersonHasLicence(sin):
			print("The person already has a licence")
			return
		driver_licence['sin'] = sin #Add sin to dictionary
		licence_class = input("Please enter Licence Class:")
		while ( len(licence_class)>10 or licence_class == ""): #Check if the licence class is valid or not
			print ("The Licence Class that you entered is invalid. Please try again.")
			licence_class = input("Please enter Licence Class:")
		driver_licence['class'] = licence_class  #Add licence class to the dictionary
		photo_name = input("Please insert photo for licence (Optional) :")
		issuing_date = input("Please enter issuing date of the licence in MM-DD-YYYY format:")
		while (self.is_date_valid(issuing_date) == False): #check if it is in MM-DD-YYYY format
			print ("Issuing Date that you entered is invalid. Please try again.")
			issuing_date = input("Please enter issuing date of the licence in MM-DD-YYYY format:")
		driver_licence['issuing_date'] = parse(issuing_date, dayfirst = False)
		expiring_date = input("Please enter expiring date of the licence in MM-DD-YYYY format:")
		while (self.is_date_valid(expiring_date) == False ): #check if it is in MM-DD-YYYY format
			print ("Expiring Date that you entered is invalid. Please try again.")
			expiring_date = input("Please enter expiring date of the licence in MM-DD-YYYY format:")
		driver_licence['expiring_date'] = parse(expiring_date, dayfirst = False)
		print("Wait, we are processing...")
		try: 
			if (photo_name == ""):
				photo = None
			else:
				f_photo = open(photo_name, 'rb')
				photo = f_photo.read()
				driver_licence['photo'] = photo
			
			self.comm.insert(driver_licence, 'drive_licence')
			print("Successfully registered the new driver licence #", driver_licence['licence_no'])
		except IOError as io_err:
			print("The photo that you are trying to upload does not exist.")
		except cx_Oracle.DatabaseError as exc:
			[error] = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)
		

	# get info for new vehicle registration 
	def vehicleReg(self):
		# create vehicle dictionary to store info
		vehicle = {}
		
		# get vehicle serial_no
		serial_no = input("Please enter the serial number of the vehicle: ")
		while( len(serial_no) > 15 or serial_no == ""): #if serial_no is invalid
			print("The serial number that you have entered is invalid. Please try again.")
			serial_no = input("Please enter the serial number of the vehicle: ")
		vehicle['serial_no'] = serial_no
		# need to check if vehicle is in database 
		if (self.checkVehicleReg(serial_no) == False):
			# if returns false we are ok 
			pass
		# else display corect error message 
		else:
			print("serial number already in the system!")
			return 
		# get vehicle make 
		maker = input("Please enter the make of the vehicle: ")
		while( len(maker) > 20 or maker == ""): #if maker is invalid
			print("The make that you have entered is invalid. Please try again.")
			maker = input("Please enter the make of the vehicle: ")
		vehicle['maker'] = maker
		# get vehicle model
		model = input("Please enter the model of the vehicle: ")
		while( len(model) > 20 or model == ""): #if model is invalid
			print("The model that you have entered is invalid. Please try again.")
			model = input("Please enter the model of the vehicle: ")
		vehicle['model'] = model
		# get vehicle year
		year = int(input("Please enter the year of the vehicle: "))
		while( year > 9999 or year < 1): #if year is not between 1-4 digits 
			print("The year that you have entered is invalid. Please try again.")
			year = int(input("Please enter the year of the vehicle: "))
		vehicle['year'] = year
		# get vehicle color 
		color = input("Please enter the color of the vehicle: ")
		while( len(color) > 10 or color == ""): # if color is invalid
			print("The color that you have entered is invalid. Please try again.")
			color = input("Please enter the color of the vehicle: ")
		vehicle['color'] = color
		# get type_id
		while(True):
			try:
				type_id = int(input("Please enter the type_id: "))
				break
			except ValueError:
				print("The type_id is invalid. Please try again.")
				type_id = int(input("Please enter the type_id: "))
		vehicle['type_id'] = type_id
		
		# add the vehicle to database
		self.comm.insert(vehicle, 'vehicle')
		print("Vehicle with serial # ", serial_no, " successfully registered.")		
		# create owner dictionary to store info
		owner = {}
		owner['vehicle_id'] = serial_no
		# loop to keep adding owners 
		while(True):
			# deal with primary and secondary owners 
			owner = self.addOwner(owner, 0)
			self.comm.insert(owner, 'owner')
			try:
				self.comm.insert(owner, 'owner')
				print("Owner added.")
			except cx_Oracle.DatabaseError as exc:
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				#print( sys.stderr, "Oracle message:", error.message)
				print("This person is already an owner of this vehicle.")
			another = input('Would you like to add another owner? (y or n)')
			if (another == 'n'):
				break
			
	def violationRec(self):
		
		#TODO No violator identified

		ticket = {}

		ticket['ticket_no'] = self.comm.getNewID('ticket', 'ticket_no')

		temp = input("Serial # of the vehicle involved: ")
		while( len(temp) > 15 or temp == "" ):
			print("The serial # that you entered is invalid. Please try again.")
			temp = input("Serial # of the vehicle involved: ")
		if not self.checkVehicleReg(temp):
			print("This vehicle is not registered. Please register the vehicle first.")
			return
		ticket['vehicle_id'] = temp

		temp = input("SIN of the violator: ")
		while( len(temp) > 15 or temp == "" ):
			print("The SIN that you entered is invalid. Please try again.")
			temp = input("SIN of the violator: ")
		if not self.checkPersonReg(temp):
			print("This person is not registered.")
			return
		ticket['violator_no'] = temp

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

		temp = input("Date of the violation (mm-dd-yyyy): ")
		while (self.is_date_valid(temp) == False): 
			print ("The date entered is invalid. Please try again.")
			temp = input("Date of the violation (mm-dd-yyyy): ")
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

		try:
			self.comm.insert(ticket, 'ticket')
			print("Successfully entered ticket #", ticket['ticket_no'])
		except cx_Oracle.DatabaseError as exc:
			error=exc.args
			#print( sys.stderr, "Oracle code:", error.code)
			#print( sys.stderr, "Oracle message:", error.message)
			print("Oops, something went wrong.")

	def searchEngine(self):
		while(True):
			print("Select an option:")
			print("1. Search driver information by name")
			print("2. Search driver information by licence number")
			print("3. Search violation records by licence number")
			print("4. Search violation records by SIN")
			print("5. Search vehicle history by serial number")
			print("6. Return to main menu")
			try:
				choice = int(input("Choose a number: "))
			except ValueError:
				choice = 0

			while (choice > 6 or choice < 1):
				try:
					choice = int(input("Choice not valid. Please choose a number between 1-6: "))
				except ValueError:
					choice = 0

			if choice == 6:
				break

			print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("                 <<< ", self.searchChoices[choice], " >>>\n")


			while(True):
				term = input("Enter search term or leave blank to go back: ")
				if not term == "":
					self.comm.search(choice, term)
				else:
					break
				print()
			print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
