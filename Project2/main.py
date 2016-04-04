import sys
from bsddb3 import db
import random

# Make sure you run "mkdir /tmp/msabbasi_db" first!
DA_FILE = "/tmp/msabbasi_db/testing_db"
DB_SIZE = 1000
SEED = 10000000

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def create_database(mode):
    try:
        # create a btree file
        if mode == 'btree':
            database.open(DA_FILE,None, db.DB_BTREE, db.DB_CREATE)
        elif mode == 'hash':
            database.open(DA_FILE,None, db.DB_HASH, db.DB_CREATE)
            
    except:
        print("Error creating file.")
        sys.exit()

    random.seed(SEED)

    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        #print (key)
        #print (value)
        #print ("")
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        database.put(key, value);

def destroy_database():
    try:
        database.close()
    except Exception as e:
        print (e)

def main():
    if len(sys.argv) < 2:
        print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
        sys.exit()
    else:
        mode = sys.argv[1]
        if mode != 'btree' and mode != 'hash' and mode != 'indexfile':
            print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
            sys.exit()

    database = db.DB()

    while(True):
	    print()
	    print("====================================================================")
	    print("                               MAIN MENU                            ")
	    print("====================================================================")

	    # Get the user to choose an option
	    try:
		    choice = int(input("""Please select the number corresponding to your choice: \n1 - Create and populate a database \n2 - Retrieve records with a given key \n3 - Retrieve records with a given data \n4 - Retrieve records with a given range of key values \n5 - Destroy the database \n6 - Quit \nType a number: """ ))
	    except ValueError:
		    choice = 0
	    while (choice > 6 or choice < 1):
		    try:
			    choice = int(input("Choice not valid. Please choose a number between 1-6: "))
		    except ValueError:
			    choice = 0

	    # Exit if exit option choosen
	    if choice == 6:
		    print("Exiting...")
		    break
        elif choice == 1:
            create_database(mode)
        elif choice == 2:
    	    print(choice)
        elif choice == 3:
    	    print(choice)
        elif choice == 4:
    	    print(choice)
        elif choice == 5:
    	    destroy_database()

	    # Start the app supplying the choice and the communicator
	    #app = App(choice, communication)
	    #result = app.run()

	    # Exit if the user choose to quit
	    #if result == 0:
	    #	break
	

    # Clean up


if __name__ == "__main__":
    main()

