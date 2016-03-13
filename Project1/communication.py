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
				self.curs1.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description dl.expiring_date FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE p.name = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id")
				self.curs2 = self.connection.cursor()
				self.curs2.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description dl.expiring_date FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE dl.licence_no = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id")
				self.curs3 = self.connection.cursor()
				self.curs3.prepare("SELECT * FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE p.name = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id")
				self.curs4 = self.connection.cursor()
				self.curs4.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description dl.expiring_date FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE p.name = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id")
				self.curs5 = self.connection.cursor()
				self.curs5.prepare("SELECT p.name, dl.licence_no, p.addr, p.birthday, dc.description dl.expiring_date FROM people p, drive_licence dl, driving_condition dc, restriction r WHERE p.name = :variable AND p.sin = dl.sin AND dl.licence_no = r.licence_no AND r.r_id = dc.c_id"")
				
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				print("Oracle message:", error.message)

	def insert(self, table, name):
		try:
			statement = 'insert into ' + name + '('
			values = ' values('
			for key in table:
				statement+= key +', '
				if key == 'photo':
					self.curs.setinputsizes(image=cx_Oracle.BLOB)
				if isinstance(table[key], str):
					values+= "'" + table[key] +"', "
				elif isinstance(table[key], datetime):
					values+= "date '" + table[key].strftime("%y-%m-%d") +"', "
				else:
					values+= str(table[key]) +', '
			statement = statement[:-2]
			values = values[:-2]
			statement += ') ' + values + ')'
	
			#print(statement)
			self.curs.execute(statement)
			self.connection.commit()
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	

	def getNewID(self, tableName, column):
		try:
			statement = 'select ' + column + ' from ' + tableName
			self.cursListKeys.execute(statement)
			rows = self.cursListKeys.fetchall()

			if len(rows) == 0:
				if dataType == 'CHAR':
					return '0'
				else:
					return 0

			ids = []

			for row in rows:
				if dataType == 'CHAR':
					ids.append(int(row[0]))
				else:
					ids.append(row[0])

			ids.sort()
			return str(ids[len(ids)-1] +1)
			
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
			rows = self.curs1.fetchall();
		elif mode == 3:
			self.curs3.execute(None, {'variable':term})
			rows = self.curs1.fetchall();
		elif mode == 4:
			self.curs4.execute(None, {'variable':term})
			rows = self.curs1.fetchall();
		else mode == 5:
			self.curs5.execute(None, {'variable':term})
			rows = self.curs1.fetchall();

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
