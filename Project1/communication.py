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
				self.cursID = self.connection.cursor()
				self.cursID.prepare("SELECT cols.column_name, atc.data_type FROM all_constraints cons, all_cons_columns cols, all_tab_columns atc WHERE cols.table_name = :tableName AND atc.table_name = cols.table_name AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND atc.owner = :username AND cons.owner = cols.owner AND atc.owner = cols.owner ORDER BY cols.table_name, cols.position")
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				print("Oracle message:", error.message)

	def insert(self, table, name):
		try:
			curs = self.connection.cursor()
			statement = 'insert into ' + name + '('
			values = ' values('
			for key in table:
				statement+= key +', '
				if key == 'photo':
					curs.setinputsizes(image=cx_Oracle.BLOB)
				if isinstance(table[key], str):
					values+= "'" + table[key] +"', "
				elif isinstance(table[key], datetime):
					values+= "date '" + table[key].strftime("%y-%m-%d") +"', "
				else:
					values+= str(table[key]) +', '
			statement = statement[:-2]
			values = values[:-2]
			statement += ') ' + values + ')'
	
			print(statement)
			curs.execute(statement)
			self.connection.commit()		
			curs.close()
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	

	def getNewID(self, tableName):
		try:
			self.cursID.execute(None, {'tableName':tableName.upper(), 'username':self.user})
			rows = self.cursID.fetchall()
			for row in rows:
				print(row)
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	
		return

	def teardown(self):
		#curs.close()
		self.connection.close()
