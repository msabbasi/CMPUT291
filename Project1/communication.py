import sys
from datetime import *
import cx_Oracle
import getpass

class Comm:
	def __init__(self, mode):
		self.authMode = mode

	# Authenticate, establish a connection, and prepare cursors
	def authenticate(self):
		successful = False
		while(not successful):
			# Get username and password
			user = input("Username: " )
			password = getpass.getpass()
			connString = ''+user+'/'+ password +'@gwynne.cs.ualberta.ca:1521/CRS'
			try:
				successful = True
				self.connection = cx_Oracle.connect(connString)
				self.user = user

				# Prepare various cursors for various tasks
				self.curs = self.connection.cursor()
				self.cursListKeys = self.connection.cursor()
				self.curs1 = self.connection.cursor()
				self.curs1.prepare('SELECT p.name, p.birthday, dl.licence_no, dl.class, dl.expiring_date, dc.description , p.addr FROM people p, drive_licence dl, restriction r, driving_condition dc WHERE p.sin = dl.sin AND r.licence_no (+)= dl.licence_no AND dc.c_id (+)= r.r_id AND upper(p.name) = :variable')
				self.curs2 = self.connection.cursor()
				self.curs2.prepare("SELECT p.name, p.birthday, dl.licence_no, dl.class, dl.expiring_date, dc.description , p.addr FROM people p, drive_licence dl, restriction r, driving_condition dc WHERE p.sin = dl.sin AND r.licence_no (+)= dl.licence_no AND dc.c_id (+)= r.r_id AND dl.licence_no = :variable ")
				self.curs3 = self.connection.cursor()
				self.curs3.prepare("SELECT t.*, tt.fine FROM drive_licence dl, ticket t, ticket_type tt WHERE dl.licence_no = :variable AND t.violator_no (+)= dl.sin AND t.vtype = tt.vtype")
				self.curs4 = self.connection.cursor()
				self.curs4.prepare("SELECT t.*, tt.fine FROM people p, ticket t, ticket_type tt WHERE p.sin = :variable AND t.violator_no (+)= p.sin  AND t.vtype = tt.vtype")
				self.curs5 = self.connection.cursor()
				self.curs5.prepare("SELECT count(DISTINCT transaction_id), avg(price), count(DISTINCT t.ticket_no) FROM vehicle h, auto_sale a, ticket t WHERE t.vehicle_id (+) = h.serial_no AND a.vehicle_id (+) = h.serial_no GROUP BY h.serial_no HAVING h.serial_no = :variable ")
				
			# Display appropriate error message according to the error code
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				if error.code == 1017:
					print("Invalid username or password. Please try again.")
				else:
					print("Sorry, there was a problem. Please try again.")

	# Given the table name and a dictionary with its values, insert the table into the database
	def insert(self, table, name):

		# Put together the statement
		photo = None
		statement = 'insert into ' + name + '('
		values = ' values('
		for key in table:
			statement+= key +', '
			# check type of each value to take into account additional requirements
			if key == 'photo':
				self.curs.setinputsizes(photo=cx_Oracle.BLOB)
				photo = table[key]
				values+= ":photo, "
			elif isinstance(table[key], str):
				values+= "'" + table[key] +"', "
			elif isinstance(table[key], datetime):
				values+= "date '" + table[key].strftime("%y-%m-%d") +"', "
			else:
				values+= str(table[key]) +', '
		statement = statement[:-2]
		values = values[:-2]
		statement += ') ' + values + ')'

		# If a photo is to be inserted, use a binding variable
		if photo == None:
			self.curs.execute(statement)
		else:
			self.curs.execute(statement, {'photo':photo})
		self.connection.commit()

	# Returns a new unique primary key given the table name and primary key column
	def getNewID(self, tableName, column):
		try:
			# form and execute the query
			statement = 'select ' + column + ' from ' + tableName
			self.cursListKeys.execute(statement)
			rows = self.cursListKeys.fetchall()

			# there are no rows in the table so let's start with 0
			if len(rows) == 0:
				return 0

			ids = []

			# add all existing ids in a list and return 1 + max
			for row in rows:
				ids.append(int(row[0]))

			ids.sort()
			return str(ids[len(ids)-1] +1)
			
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	
		return

	# Executes the mode's respective prepared cursor and displays results in a user friendly way
	def search(self, mode, term):

		if mode == 1:
			# binding variable used along with upper() to allow case insensitive search
			self.curs1.execute(None, {'variable':term.upper()})
			rows = self.curs1.fetchall()
			# display column names
			print("________________________________________________________________________________________________________________________")
			print("     Name      | Birthday |   Licence #   |    Class    |Expiry Date|        Condition         |   Address   ")
			print("````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
			licNo = None
			# display all the fields with the right amount of spaces in between
			for row in rows:
				if row[1] == licNo:
					print("               |          |               |           |           |"+str(row[4])+" "*(26-len(str(row[4])))+"|")
				else:				
					print(row[0]+" "*(15-len(row[0]))+"|"+row[1].strftime('%m/%d/%Y')+"  "+"|"+row[2]+" "*(15-len(row[2]))+"|"+row[3]+" "*(13-len(row[3]))+"|"+row[4].strftime('%m/%d/%Y')+"   "+"|"+str(row[5])+" "*(26-len(str(row[5])))+"|"+row[6])
				licNo = row[1]
	
		elif mode == 2:
			self.curs2.execute(None, {'variable':int(term)})
			rows = self.curs2.fetchall()
			print("______________________________________________________________________________________________________________________")
			print("     Name      | Birthday |   Licence #   |    Class    |Expiry Date|        Condition         |   Address   ")
			print("``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
			licNo = None
			for row in rows:
				if row[1] == licNo:
					print("               |          |               |           |           |"+str(row[4])+" "*(26-len(str(row[4])))+"|")
				else:				
					print(row[0]+" "*(15-len(row[0]))+"|"+row[1].strftime('%m/%d/%Y')+"  "+"|"+row[2]+" "*(15-len(row[2]))+"|"+row[3]+" "*(13-len(row[3]))+"|"+row[4].strftime('%m/%d/%Y')+"   "+"|"+str(row[5])+" "*(26-len(str(row[5])))+"|"+row[6])
				licNo = row[1]

		elif mode == 3:
			self.curs3.execute(None, {'variable':int(term)})
			rows = self.curs3.fetchall()
			print("___________________________________________________________________________________________________________________________________________________")
			print(" Ticket #  |  Violator SIN |   Vehicle #   |  Officer SIN  |  Violation |   Date   |        Place        |            Description        | Fine   ")
			print("```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
			for row in rows:
				print(str(row[0])+" "*(11-len(str(row[0])))+"|"+row[1]+" "*(15-len(row[1]))+"|"+row[2]+" "*(15-len(row[2]))+"|"+row[3]+" "*(15-len(row[3]))+"|"+row[4]+" "*(12-len(row[4]))+"|"+row[5].strftime('%m/%d/%Y')+"  "+"|"+row[6]+" "*(21-len(row[6]))+"|"+row[7]+" "*(31-len(row[7]))+"|"+str(row[8]))

		elif mode == 4:
			self.curs4.execute(None, {'variable':int(term)})
			rows = self.curs4.fetchall()
			print("___________________________________________________________________________________________________________________________________________________")
			print(" Ticket #  |  Violator SIN |   Vehicle #   |  Officer SIN  |  Violation |   Date   |        Place        |            Description        | Fine   ")
			print("```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````")
			for row in rows:
				print(str(row[0])+" "*(11-len(str(row[0])))+"|"+row[1]+" "*(15-len(row[1]))+"|"+row[2]+" "*(15-len(row[2]))+"|"+row[3]+" "*(15-len(row[3]))+"|"+row[4]+" "*(12-len(row[4]))+"|"+row[5].strftime('%m/%d/%Y')+"  "+"|"+row[6]+" "*(21-len(row[6]))+"|"+row[7]+" "*(31-len(row[7]))+"|"+str(row[8]))

		else:
			self.curs5.execute(None, {'variable':int(term)})
			rows = self.curs5.fetchall()
			print("_________________________________________________________")
			print("   Times sold   |   Avg Price   |  Violations involved in")
			print("`````````````````````````````````````````````````````````")
			for row in rows:
				print(str(row[0])+ " "*(16-len(str(row[0])))+ "|"+ str(row[1])+ " "*(15-len(str(row[1])))+ "|"+ str(row[2]))	


		if len(rows) == 0:
			print("No results found.")
			return

	# Clean up
	def teardown(self):
		self.curs.close()
		self.curs1.close()
		self.curs2.close()
		self.curs3.close()
		self.curs4.close()
		self.curs5.close()
		self.cursListKeys.close()
		self.connection.close()


