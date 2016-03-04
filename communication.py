import cx_Oracle
import getpass

class Comm:
	def __init__(self, mode):
		self.authMode = mode

	def authenticate(self):
		successful = True
		while(not successful):
			user = input("Username [%s]: " % getpass.getuser())
			if not user:
				user = getpass.getuser()
			password = getpass.getpass()
			connString = ''+user+'/'+ pw +'@gwynne.cs.ualberta.ca:1521/CRS'
			try:
				successful = True
				self.connection = cx_Oracle.connect(connString)
			except cx_Oracle.DatabaseError as exc:
				successful = False
				error, = exc.args
				print( sys.stderr, "Oracle code:", error.code)
				print( sys.stderr, "Oracle message:", error.message)

	def teardown(self):
		curs.close()
		connection.close()
