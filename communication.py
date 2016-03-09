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

	def insert(self, table):
		curs = self.connection.cursor()
		curs.close()
		

	def execute(self):
		curs = self.connection.cursor()
		#curs.execute("insert into movie(TITLE, movie_number) values('Spiderman', 1)")
		#self.connection.commit()
		#curs.execute("SELECT * from movie")
		#rows = curs.fetchall()
		#for row in rows:
		#	print(row)
		curs.close()

	def getNewID(self, tableName):
		#http://stackoverflow.com/questions/9016578/how-to-get-primary-key-column-in-oracle
		return

	def teardown(self):
		#curs.close()
		self.connection.close()
