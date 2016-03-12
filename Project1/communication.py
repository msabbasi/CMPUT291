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
				self.cursKey = self.connection.cursor()
				self.cursListKeys = self.connection.cursor()
				self.cursKey.prepare("SELECT cols.column_name, atc.data_type FROM all_constraints cons, all_cons_columns cols, all_tab_columns atc WHERE cols.table_name = :tableName AND atc.table_name = cols.table_name AND cons.constraint_type = 'P' AND cons.constraint_name = cols.constraint_name AND cols.column_name = atc.column_name AND cons.owner = cols.owner ORDER BY cols.table_name, cols.position")
				#self.cursListKeys.prepare("SELECT :keyColumn FROM :tableName")
				
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
	
			print(statement)
			self.curs.execute(statement)
			self.connection.commit()
		except cx_Oracle.DatabaseError as exc:
			error, = exc.args
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)	

	def getNewID(self, tableName):
		try:
			self.cursKey.execute(None, {'tableName':tableName.upper()})
			rows = self.cursKey.fetchall()
			column = rows[0][0]
			dataType = rows[0][1]

			print(column)
			print(dataType)
			print(tableName.upper())

			statement = 'select ' + column + ' from ' + tableName
			self.cursListKeys.execute(statement)
			#self.cursListKeys.execute(None, {'keyColumn':column, 'tableName':tableName})
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

	def teardown(self):
		self.curs.close()
		self.cursKey.close()
		self.cursListKeys.close()
		self.connection.close()
