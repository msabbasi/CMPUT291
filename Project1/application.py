

class App:
	

	def __init__(self, mode, communicator):
		self.appMode = mode
		self.comm = communicator

	def run(self):
		checkReg = (input("Is the seller registered? (y/n) "))
		people = {'sin': 'abcd', 'name': 'abcd', 'height': 5.20, 'weight': 5.20, 'eyecolor': 'blue', 'haircolor': 'brown', 'addr': '123 45 Ave NW, Edmonton', 'gender': '?', 'birthday': '12-03-96'}
		if (checkReg == 'n'):
			people['name'] = input("Name: ")
			people['gender'] = input["Gender(f/m): ")
			people[''] = input("Name: ")
		
