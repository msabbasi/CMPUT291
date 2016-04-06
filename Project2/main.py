import sys
import time
from bsddb3 import db
import random

# Make sure you run "mkdir /tmp/msabbasi_db" first!
DA_FILE = "/tmp/msabbasi_db/testing_db"
DB_SIZE = 1000
SEED = 10000000
answers = open("answers", "w")
choices = {1: 'Create and populate database', 2: 'Retrieve records with a given key', 3: 'Retrieve records with a given data', 4: 'Retrieve records with a given range of key values', 5: 'Destroy the database', 6: 'Quit'}

# Helper functions
def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))
#TODO: Write a function that writes results to a file
def write_answers(ResultToWrite):
    answers.writelines(ResultToWrite)
    return
def getData(result):
    pivot = result.find("'")
    return result[pivot:]

# Create and populate database
def create_database(mode, database):
    try:
        if mode == 'btree':
            database.open(DA_FILE, None, db.DB_BTREE, db.DB_CREATE)
        elif mode == 'hash':
            database.open(DA_FILE, None, db.DB_HASH, db.DB_CREATE)    
    except:
        print("Error creating file.")
        sys.exit()

    random.seed(SEED)

    #TODO: Display key/data pairs randomly to help search later

    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        print (key)
        print (value)
        print ("")
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        database.put(key, value);

# Remove the database
def destroy_database(database):
    try:
        database.close()
        database.remove(DA_FILE, None)
    except Exception as e:
        print (e)

#TODO: Fill the following functions with a loop that asks for information and diplays result

def search_key(database):
    while(True):
        key = input("Key (leave empty to return): ")
        if key == "":
            break
        start_time = time.time()
        result = database.get(key.encode(encoding='UTF-8'))
        stop_time = time.time()
        #theData = getData(result)
        #write_answers([key+ "\n",theData+"\n","\n"])
        #answer.close()
        print(result.decode("utf-8"))
        print("Number of records retrieved: 1")
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds") 

def search_data(database):
    print("search data")

def search_range(database):
    print("retrieve range")

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
        print("============================================================================")
        print("                                    MAIN MENU                               ")
        print("============================================================================")

        # Get the user to choose an option
        try:
            for key in choices:
                print(key, ': ', choices[key])
            choice = int(input("\nPlease select the number corresponding to your choice: "))
        except ValueError:
            choice = 0
        while (choice > 6 or choice < 1):
            try:
                choice = int(input("Choice not valid. Please choose a number between 1-6: "))
            except ValueError:
                choice = 0

        # Exit if exit option choosen
        if choice == 6:
            print("Exiting...\n")
            break

        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("               ", choices[choice])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")        

        if choice == 1:
            create_database(mode, database)
        elif choice == 2:
            search_key(database)
        elif choice == 3:
            search_data(database)
        elif choice == 4:
            search_range(database)
        elif choice == 5:
            destroy_database(database)

    #TODO: Clean up nicely when terminating


if __name__ == "__main__":
    main()

