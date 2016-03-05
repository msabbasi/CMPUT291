import sys
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
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				#print( sys.stderr, "Oracle code:", error.code)
				print("Oracle message:", error.message)

	def teardown(self):
		#curs.close()
		self.connection.close()
