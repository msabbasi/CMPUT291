import sys
from datetime import *
import cx_Oracle
import getpass

class Comm:
	def __init__(self, mode):
		self.authMode = mode

	def authenticate(self):
		successful = False
		while(not successful):
			user = input("Username: " )
			password = getpass.getpass()
			connString = ''+user+'/'+ password +'@gwynne.cs.ualberta.ca:1521/CRS'
			try:
				successful = True
				self.connection = cx_Oracle.connect(connString)
				self.user = user			
				self.curs = self.connection.cursor()
				self.cursListKeys = self.connection.cursor()
				self.curs1 = self.connection.cursor()
				self.curs1.prepare('SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description , dl.expiring_date FROM people p, drive_licence dl, restriction r, driving_condition dc WHERE p.sin = dl.sin AND r.licence_no (+)= dl.licence_no AND dc.c_id (+)= r.r_id AND p.name =:variable')
				self.curs2 = self.connection.cursor()
				self.curs2.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description , dl.expiring_date FROM people p, drive_licence dl, restriction r, driving_condition dc WHERE p.sin = dl.sin AND r.licence_no (+)= dl.licence_no AND dc.c_id (+)= r.r_id AND dl.licence_no = :variable ")
				self.curs3 = self.connection.cursor()
				self.curs3.prepare("SELECT t.*, tt.fine FROM people p, ticket t, ticket_type tt WHERE p.name = :variable AND p.sin = t.violator_no AND t.vtype = tt.vtype")
				self.curs4 = self.connection.cursor()
				self.curs4.prepare("SELECT t.*, tt.fine FROM people p, ticket t, ticket_type tt WHERE p.sin = :variable AND p.sin = t.violator_no AND t.vtype = tt.vtype")
				self.curs5 = self.connection.cursor()
				self.curs5.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description, dl.expiring_date FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE p.name = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id")
				
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				if error.code == 1017:
					print("Invalid username or password. Please try again.")
				else:
					print("Sorry, there was a problem. Please try again.")

	def insert(self, table, name):
		photo = None
		statement = 'insert into ' + name + '('
		values = ' values('
		for key in table:
			statement+= key +', '
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

		print(statement)
		if photo == None:
			self.curs.execute(statement)
		else:
			self.curs.execute(statement, {'photo':photo})
		self.connection.commit()

	def getNewID(self, tableName, column):
		try:
			statement = 'select ' + column + ' from ' + tableName
			self.cursListKeys.execute(statement)
			rows = self.cursListKeys.fetchall()

			if len(rows) == 0:
				return 0

			ids = []

			for row in rows:
				ids.append(row[0])

			ids.sort()
			return str(int(ids[len(ids)-1]) +1)
			
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	
		return

	def search(self, mode, term):
		if mode == 1:
			self.curs1.execute(None, {'variable':term})
			rows = self.curs1.fetchall();		    			
		elif mode == 2:
			self.curs2.execute(None, {'variable':term})
			rows = self.curs2.fetchall();
		elif mode == 3:
			self.curs3.execute(None, {'variable':term})
			rows = self.curs3.fetchall();
		elif mode == 4:
			self.curs4.execute(None, {'variable':term})
			rows = self.curs4.fetchall();
		else:
			self.curs5.execute(None, {'variable':term})
			rows = self.curs5.fetchall();

		if len(rows) == 0:
			print("No results found.")
			return

		for row in rows:
			print(row)

	def teardown(self):
		self.curs.close()
		self.curs1.close()
		self.curs2.close()
		self.curs3.close()
		self.curs4.close()
		self.curs5.close()
		self.cursListKeys.close()
		self.connection.close()


