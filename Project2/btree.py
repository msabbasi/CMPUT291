# Berkeley DB Example
# Edited: 21 March 2016  by Kriti
__author__ = "Bing Xu"
__email__ = "bx3@ualberta.ca"

from bsddb3 import db
import random
# Make sure you run "mkdir /tmp/my_db" first!
DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))


def main():
    database = db.DB()
    try:
        # create a btree file
        database.open(DA_FILE,None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Error creating file.")

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

    # retriving all values
    cur = database.cursor()
    iter = cur.first()
    while iter:
       print(iter[0].decode("utf-8"))
       print(iter[1].decode("utf-8"))
       iter = cur.next()
    print("------------------------")
    try:
        database.close()
    except Exception as e:
        print (e)

if __name__ == "__main__":
    main()
