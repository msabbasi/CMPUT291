import sys
import time
from bsddb3 import db
import random
import shutil
import os
import numpy

DA_FILE = "/tmp/msabbasi_db/testing_db"
DA_FILE_S = "/tmp/msabbasi_db/secondary_db"
DB_SIZE = 100000
SAMPLE_SIZE = 10
SEED = 10000000
choices = {1: 'Create and populate database', 2: 'Retrieve records with a given key', 3: 'Retrieve records with a given data', 4: 'Retrieve records with a given range of key values', 5: 'Destroy the database', 6: 'Quit'}

# Helper functions
# get random int 
def get_random():
    return random.randint(0, 63)
# get random char 
def get_random_char():
    return chr(97 + random.randint(0, 25))
# function to help write to our answers file 
def write_answers(ResultToWrite):
    answers = open("answers", "a")
    for each in ResultToWrite:
        answers.write(str(each[0]))
        answers.write('\n')
        answers.write(str(each[1]))
        answers.write('\n')
        answers.write('\n')
    answers.close()
# return data based on the key
def get_data(primarykey, primarydata):
    return primarydata

# Create and populate database
def create_database(mode):
    database_creator = db.DB()
    sec_db_creator = None
    try:
        if mode == 'btree':
            database_creator.open(DA_FILE, None, db.DB_BTREE, db.DB_CREATE)
        elif mode == 'hash':
            database_creator.open(DA_FILE, None, db.DB_HASH, db.DB_CREATE)
        elif mode == 'indexfile':
            database_creator.open(DA_FILE, None, db.DB_BTREE, db.DB_CREATE)
            sec_db_creator = db.DB()
            # Allow the secondary index to have duplicates
            sec_db_creator.set_flags(db.DB_DUP)
            sec_db_creator.open(DA_FILE_S, None, db.DB_HASH, db.DB_CREATE)
    except Exception as e:
        print (e)
        print("Error creating file.")
        sys.exit()

    random.seed(SEED)

    print("Sample entries for testing:\n")
    # generate the data 
    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        ekey = key.encode(encoding='UTF-8')
        evalue = value.encode(encoding='UTF-8')
        if not database_creator.exists(ekey):
            # Display a few of the entries to be used in testing
            if index % (DB_SIZE/SAMPLE_SIZE) == 0:
                print (key)
                print (value)
                print ("")
            database_creator.put(ekey, evalue)
            if sec_db_creator != None:
                sec_db_creator.put(evalue, ekey)
    database_creator.close()
    if sec_db_creator != None:
        sec_db_creator.close()

# Remove the database
def destroy_database(quitting):    
    global mode
    database_remover = db.DB()
    sec_db_remover = db.DB()
    try:
        database_remover.remove(DA_FILE, None)
        if mode == 'indexfile':
            sec_db_remover.remove(DA_FILE_S, None)
        database_remover.close()
        sec_db_remover.close()
        print("Database successfully destroyed.")
    except Exception as e:
        if not quitting:
            print ("Database does not exist.")

# function to perform a key search
def search_key(database):
    while(True):
        record = 1
        key = input("\nKey (leave empty to return): ")
        if key == "":
            break
        start_time = time.time()
        result = database.get(key.encode(encoding='UTF-8'))
        stop_time = time.time()
        try:
            write_answers([(key,result.decode("utf-8"))])
        except AttributeError:
            record = 0
        print("Number of records retrieved:", record)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")

# function to perform a data search
def search_data(database):
    while(True):
        numbKeys = 0
        value = input("\nValue (leave empty to return): ")
        if value == "":
            break
        result = []
        cur = database.cursor()
        start_time = time.time()
        pair = cur.first()
        # Go through all key/data pairs to search for data matches
        while pair:
            key = pair[0].decode("utf-8")
            data = pair[1].decode("utf-8")
            if data == value:
                result.append((key,data))
                numbKeys = numbKeys + 1
            pair = cur.next()
        stop_time = time.time()
        write_answers(result)
        print("Number of records retrieved: ", numbKeys)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")
# function to perform a data search with our indexfile
def search_data_index(database):
    while(True):
        record = 0
        key = input("\nValue (leave empty to return): ")
        if key == "":
            break
        results = []
        cur = database.cursor()
        start_time = time.time()
        # Search the secondary index for the data
        result = cur.set(key.encode(encoding='UTF-8'))
        while result:
            results.append((result[1].decode("utf-8"),result[0].decode("utf-8")))
            record = record + 1
            # Check if any duplicates
            result = cur.next_dup()
        stop_time = time.time()
        try:
            write_answers(results)
        except AttributeError:
            record = 0
        print("Number of records retrieved:", record)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")
# function to perform a range search
def search_range(database):
    global mode

    while(True):
        numbKeys = 0
        lower = input("\nLower key (leave empty to return): ")
        if lower == "":
            break
        upper = input("Upper key (leave empty to return): ")
        if upper == "":
            break
        # Make sure lower bound is lower than upper bound
        while lower > upper:
            print("Please enter an upper bound greater than the lower bound.")
            upper = input("Upper key (leave empty to return): ")
            if upper == "":
                return
        result = []
        cur = database.cursor()
        start_time = time.time()
        pair = cur.first()
        # Go through all records to find all keys within range
        if mode == 'hash':
            while pair:
                key = pair[0].decode("utf-8")
                data = pair[1].decode("utf-8")
                if key >= lower and key <= upper:
                    result.append((key, data))
                    numbKeys = numbKeys + 1
                pair = cur.next()
        # Just find the start of the lower limit and retrieve data up to the upper limit
        elif mode == 'btree' or mode == 'indexfile':
            while pair and pair[0].decode("utf-8") < lower:
                pair = cur.next()
            while pair and pair[0].decode("utf-8") <= upper:
                key = pair[0].decode("utf-8")
                data = pair[1].decode("utf-8")
                result.append((key, data))
                numbKeys = numbKeys + 1
                pair = cur.next()
        stop_time = time.time()
        write_answers(result)
        print("Number of records retrieved: ", numbKeys)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")
# destroy database and cleanup results
def cleanup():
    try:
        destroy_database(True)
    except:
        pass
    shutil.rmtree('/tmp/msabbasi_db')
    print("/tmp/msabbasi_db removed.")
    print("Clean up complete.")

def main():
    global mode

    if len(sys.argv) < 2:
        print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
        sys.exit()
    else:
        mode = sys.argv[1]
        if mode != 'btree' and mode != 'hash' and mode != 'indexfile':
            print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
            sys.exit()

    database_exists = False
    answers = open("answers", "w")
    answers.close()

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
            print("Exiting...")
            cleanup()
            break

        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("               ", choices[choice])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")        

        # Depending on the mode and the choice run the appropriate functions
        if choice == 1:
            if database_exists:
                print("Database already created.")
            else:
                create_database(mode)
                print("Database successfully created.")
                database_exists = True
                # create db handlers for the queries
                database = db.DB()
                database.open(DA_FILE)
                if mode == 'indexfile':
                    sec_db = db.DB()
                    sec_db.open(DA_FILE_S)
        elif choice == 5:
            destroy_database(False)
            database_exists = False
            # remove db handlers for the queries
            database.close()
            if mode == 'indexfile':                
                sec_db.close()
        elif not database_exists:
                print("Database not found. Please create the database first.")
        elif choice == 2:
            search_key(database)
        elif choice == 3:
            if mode == 'indexfile':
                search_data_index(sec_db)
            else:
                search_data(database)
        elif choice == 4:
            search_range(database)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
        
