import sys
import time
from bsddb3 import db
import random
import shutil
import os

DA_FILE = "/tmp/msabbasi_db/testing_db"
DB_SIZE = 100
SEED = 10000000
choices = {1: 'Create and populate database', 2: 'Retrieve records with a given key', 3: 'Retrieve records with a given data', 4: 'Retrieve records with a given range of key values', 5: 'Destroy the database', 6: 'Quit'}

answers = None
database = None
sdatabase = None

# Helper functions
def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))
def write_answers(ResultToWrite):
    answers = open("answers", "w")
    for each in ResultToWrite:
        answers.write(str(each[0]))
        answers.write('\n')
        answers.write(str(each[1]))
        answers.write('\n')
        answers.write('\n')
    answers.close()

# Create and populate database
def create_database(mode, database):
    database = db.DB()
    try:
        if mode == 'btree':
            database.open(DA_FILE, None, db.DB_BTREE, db.DB_CREATE)
        elif mode == 'hash':
            database.open(DA_FILE, None, db.DB_HASH, db.DB_CREATE)
        elif mode == 'indexfile':
            database.open(DA_FILE, None, db.DB_BTREE, db.DB_CREATE)
            data
            
    except:
        print("Error creating file.")
        sys.exit()

    random.seed(SEED)

    #TODO: Store/display key/data pairs randomly to help search later

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
        if not database.exists(key):
            database.put(key, value);

# Remove the database
def destroy_database(database):
    if not database:
        return
    try:
        database.close()
        database.remove(DA_FILE, None)
        database = None
    except Exception as e:
        print (e)

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

def search_range_hash(database):
    while(True):
        numbKeys = 0
        lower = input("\nLower key (leave empty to return): ")
        if lower == "":
            break
        upper = input("Upper key (leave empty to return): ")
        if upper == "":
            break
        result = []
        cur = database.cursor()
        start_time = time.time()
        pair = cur.first()
        while pair:
            key = pair[0].decode("utf-8")
            data = pair[1].decode("utf-8")
            if key >= lower and key <= upper:
                result.append((key, data))
                numbKeys = numbKeys + 1
            pair = cur.next()
        stop_time = time.time()
        write_answers(result)
        print("Number of records retrieved: ", numbKeys)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")

def search_range_btree(database):
    while(True):
        numbKeys = 0
        lower = input("\nLower key (leave empty to return): ")
        if lower == "":
            break
        upper = input("Upper key (leave empty to return): ")
        if upper == "":
            break
        result = []
        cur = database.cursor()
        start_time = time.time()
        pair = cur.first()
        while pair[0].decode("utf-8") < lower:
            pair = cur.next()
        while pair[0].decode("utf-8") <= upper:
            key = pair[0].decode("utf-8")
            data = pair[1].decode("utf-8")
            result.append((key, data))
            numbKeys = numbKeys + 1
            pair = cur.next()
        stop_time = time.time()
        write_answers(result)
        print("Number of records retrieved: ", numbKeys)
        print("Total execution time: ", (stop_time-start_time)*1000000, "microseconds")

def cleanup():
    if answers:
        os.remove('answers')
    if database:
        destroy_database(database)
    shutil.rmtree('/tmp/msabbasi_db')

def main():
    if len(sys.argv) < 2:
        print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
        sys.exit()
    else:
        mode = sys.argv[1]
        if mode != 'btree' and mode != 'hash' and mode != 'indexfile':
            print("Usage: mydbtest db_type_option where db_type_option can be btree, hash or indexfile")
            sys.exit()

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
            cleanup()
            break

        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("               ", choices[choice])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")        

        if choice == 1:
            if database:
                print("Database already created.")
            else:
                create_database(mode, database)
        elif choice == 5:
            destroy_database(database)
        elif not database:
                print("Database not created. Please create the database first.")
        elif choice == 2:
            search_key(database)
        elif choice == 3:
            search_data(database)
        elif choice == 4:
            if mode == 'hash':
                search_range_hash(database)
            elif mode == 'btree':
                search_range_btree(database)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
        
