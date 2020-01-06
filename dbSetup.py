import sqlite3


def build_items_db(cursor):
    cursor.execute("""CREATE TABLE if not exists items
                      (name text)""")
                      
def build_gifts_db(cursor):
    cursor.execute("""CREATE TABLE if not exists gifts
                      (villager text, item text, reaction text,
                      FOREIGN KEY(villager) references villagers(name),
                      FOREIGN KEY(item) references items(name),
                      PRIMARY KEY(villager, item))""")

def build_villagers_db(cursor):
    cursor.execute("""CREATE TABLE if not exists villagers 
               (name text PRIMARY KEY)""")
    f = open("villagers.txt")
    names = f.readlines()
    for name in names:
        cursor.execute("INSERT INTO villagers VALUES(?)", (name.strip('\n'),))
    f.close()
    
    

if __name__ == "__main__":
    conn = sqlite3.connect("SDV.db")
    c = conn.cursor()
    build_villagers_db(c)
    build_items_db(c)
    build_gifts_db(c)
    conn.commit()
conn.close()