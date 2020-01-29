import sqlite3

class SVGDatabase:

    def __init__(self, database_path):
        self.database_path = database_path
        self.cursor = self.get_cursor()
        self.build_all()
    
    def write_reactions_to_db(self, reactions):
        statement = "INSERT INTO gifts VALUES(?, ?, ?)"
        args = [(x.villager, x.item, x.reaction) for x in reactions]
        self.write_list_to_db(statement, args)
        
    def write_items_to_db(self, items):
        statement = "INSERT INTO items VALUES(?, ?, ?)"
        args = [(x.name, x.source, x.season) for x in items]
        self.write_list_to_db(statement, args)
        
    def write_list_to_db(self, statement, args):
        for arg in args:
            self.cursor.execute(statement, args)
        
    def get_cursor(self):
        self.conn = sqlite3.connect(f"{filename}.db")
        return conn.cursor()
        
    def commit(self):
        self.conn.commit()
        self.conn.close()
        
    def build_items_db(cursor):
    cursor.execute("""CREATE TABLE if not exists items(
                        name TEXT PRIMARY KEY NOT NULL, 
                        source TEXT NOT NULL,
                        season TEXT NOT NULL)""")
                      
    def build_gifts_db(cursor):
        cursor.execute("""CREATE TABLE if not exists gifts(
                            villager TEXT NOT NULL, 
                            item TEXT NOT NULL, 
                            reaction TEXT NOT NULL,
                            PRIMARY KEY(villager, item))""")
        
    def build_all():
        build_items_db()
        build_gifts_db()