import sqlite3


def build_items_db(cursor):
    cursor.execute("""CREATE TABLE if not exists items
                      (name text)""")
                      
def build_gifts_db(cursor):
    cursor.execute("""CREATE TABLE if not exists gifts
                      (villager text, item text, reaction text,
                      PRIMARY KEY(villager, item, reaction))""")

def build_villagers_db(cursor):
    cursor.execute("""CREATE TABLE if not exists villagers 
               (name text PRIMARY KEY)""")
    f = open("villagers.txt")
    names = f.readlines()
    for name in names:
        cursor.execute("INSERT INTO villagers VALUES(?)", (name.strip('\n'),))
    f.close()
    
def build_all(cursor):
    build_villagers_db(c)
    build_items_db(c)
    build_gifts_db(c)

if __name__ == "__main__":
    conn = sqlite3.connect("SDV.db")
    c = conn.cursor()
    build_gifts_db(c)
    conn.commit()
    conn.close()