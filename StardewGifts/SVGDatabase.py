import sqlite3

class SVGDatabase:
    DEFAULT_GIFT_TABLE_NAME = "gifts"
    DEFAULT_ITEM_TABLE_NAME = "items"
    DEFAULT_ITEM_SOURCES_TABLE_NAME = "sources"
    
    
    def __init__(self, 
        database_path, 
        gift_table_name = self.DEFAULT_GIFT_TABLE_NAME,
        item_table_name = self.DEFAULT_ITEM_TABLE_NAME
        item_sources_table_name = self.DEFAULT_ITEM_SOURCES_TABLE_NAME):
        
        self.gift_table_name = gift_table_name
        self.item_table_name = item_table_name
        
        self.database_path = database_path
        self.cursor = self.get_cursor()
        self.build_all()
    
    def write_reactions(self, reactions):
        statement = "INSERT INTO {} VALUES(?, ?, ?)" \
            .format(self.item_table_name)
        args = [(x.villager, x.item, x.reaction) for x in reactions]
        self.write_list(statement, args)
        
    def write_items(self, items):
        statement = "INSERT INTO {} VALUES(?, ?, ?)" \ 
            .format(self.gift_table_name)
        args = [(x.name, x.source, x.season) for x in items]
        self.write_list(statement, args)
        
    def write_sources(self, items):
        statement = "INSERT INTO {} VALUES(?, ?)" \
            .format(self.item_sources_table_name)
        args = []
        for item in items:
            for source in item.sources:
                args.append((item.name, source))
                
        self.write_list(args)
                
        
    def write_list(self, statement, args):
        """ Executes the given statement with every argument in 
        the args list. """
        
        for arg in args:
            self.cursor.execute(statement, args)
        
    def get_cursor(self):
        self.conn = sqlite3.connect(f"{filename}.db")
        return conn.cursor()
        
    def commit(self):
        self.conn.commit()
        self.conn.close()
        
    def build_items_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                        name TEXT PRIMARY KEY NOT NULL, 
                        source TEXT NOT NULL,
                        season TEXT NOT NULL)""" \ 
                        .format(self.item_table_name))
                      
    def build_gifts_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                            villager TEXT NOT NULL, 
                            item TEXT NOT NULL, 
                            reaction TEXT NOT NULL,
                            PRIMARY KEY(villager, item))""" \ 
                            .format(self.gift_table_name))
                            
    def build_item_sources_db(cursor):
        cursor.execute("""CREATE TABLE if not exists {}(
                            item TEXT NOT NULL REFERENCES {}(name), 
                            source TEXT NOT NULL,
                            PRIMARY KEY(item, source))""" \
                            .format(
                                self.item_sources_table_name,
                                "name"))
        
    def build_all():
        build_items_db()
        build_gifts_db()